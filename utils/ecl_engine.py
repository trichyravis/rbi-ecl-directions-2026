"""ECL engine — core analytics for the RBI ECL Directions, 2026.

This module is intentionally pure Python so it can be unit-tested in
isolation from Streamlit. Every function takes plain numbers / arrays and
returns plain numbers / DataFrames, ready to be displayed by the UI layer.

Reference: RBI Circular DOR.STR.REC.No.6/21.06.011/2026-27 (27-Apr-2026).

Notation
--------
PD   – Probability of Default (per period)
LGD  – Loss Given Default (fraction)
EAD  – Exposure at Default (₹)
DF   – Discount Factor   (1 / (1+EIR)^t)
EIR  – Effective Interest Rate
ECL  – Expected Credit Loss
NPA  – Non-Performing Asset (90-day backstop retained)
SICR – Significant Increase in Credit Risk (Stage 1 → Stage 2 trigger)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np
import pandas as pd

# Regulatory floor parameters from the circular --------------------------------

PD_FLOOR_12M = 0.0003          # 3 bps regulatory PD floor (Stage 1 12-month)
LGD_BACKSTOP_SECURED = 0.65
LGD_BACKSTOP_UNSECURED = 0.70
LGD_ELIGIBLE_COLLATERAL = 0.30  # cash, gold, G-sec, LIC, KVP, NSC

# Stage 1 / Stage 2 portfolio floors (Section N) -------------------------------
# Each row: (code, label, S1 floor, S2 floor) — DCCO-linked rows expressed as None.
S1_S2_FLOORS = pd.DataFrame(
    [
        ("(i)",       "Secured retail loans (100% collateral)",                         0.0040, 0.05),
        ("(ii)",      "Corporate loans",                                                0.0040, 0.05),
        ("(iii)",     "Loans to Small & Micro Enterprises",                             0.0025, 0.05),
        ("(iv)",      "Loans to Medium Enterprises",                                    0.0040, 0.05),
        ("(v)",       "Farm credit — agricultural activities",                          0.0025, 0.05),
        ("(vi)",      "Loans to Banks / NBFCs / other regulated FIs",                   0.0040, 0.05),
        ("(vii)",     "Loans against Term Deposits / LIC policies / KVP",               0.0040, 0.0040),
        ("(viii)",    "Gold loans",                                                     0.0040, 0.015),
        ("(ix)",      "State Government direct / guaranteed exposures",                 0.0040, 0.025),
        ("(x)",       "Unsecured retail loans",                                         0.0100, 0.05),
        ("(xi-a)",    "Housing loans to individuals",                                   0.0025, 0.015),
        ("(xi-b-i)",  "CRE — ADC — 150% RW exposures",                                  0.0125, np.nan),
        ("(xi-b-ii)", "CRE-Residential Housing — ADC",                                  0.0100, np.nan),
        ("(xi-c)",    "Other claims — Residential Real Estate",                         0.0040, 0.015),
        ("(xi-d)",    "Other claims — Commercial Real Estate",                          0.0040, 0.025),
        ("(xii-a)",   "Project finance — Pre-operational",                              0.0100, np.nan),
        ("(xii-b)",   "Project finance — Operational",                                  0.0040, 0.05),
        ("(xiii)",    "Central Government guarantee schemes (e.g. CGTMSE)",             0.0025, 0.0025),
        ("(xiv)",     "Restructured advances — standard",                               0.0500, 0.10),
        ("(xv)",      "Residual / other categories",                                    0.0040, 0.05),
    ],
    columns=["code", "category", "stage1_floor", "stage2_floor"],
)

# Stage 3 progressive floors --------------------------------------------------
S3_FLOORS_GENERAL = pd.DataFrame(  # Categories (i)-(vi), (xii), (xiv), (xv)
    [
        ("0–1 year",      0.25, 0.40),
        ("1–2 years",     0.40, 1.00),
        ("2–3 years",     0.55, 1.00),
        ("3–4 years",     0.75, 1.00),
        ("After 4 years", 1.00, 1.00),
    ],
    columns=["bucket", "secured", "unsecured"],
)

S3_FLOORS_LOWER = pd.DataFrame(  # Categories (vii)-(ix), (xi-a), (xiii)
    [
        ("0–1 year",      0.10, 0.25),
        ("1–2 years",     0.20, 1.00),
        ("2–3 years",     0.30, 1.00),
        ("3–4 years",     0.40, 1.00),
        ("After 4 years", 1.00, 1.00),
    ],
    columns=["bucket", "secured", "unsecured"],
)

S3_FLOORS_UNSECURED_RETAIL = pd.DataFrame(  # Category (x)
    [
        ("0–1 year",      np.nan, 0.25),
        ("After 1 year",  np.nan, 1.00),
    ],
    columns=["bucket", "secured", "unsecured"],
)

CET1_PHASE_IN = pd.DataFrame(
    [
        ("FY 2027–28", 4 / 5),
        ("FY 2028–29", 3 / 5),
        ("FY 2029–30", 2 / 5),
        ("FY 2030–31", 1 / 5),
        ("FY 2031–32+", 0.0),
    ],
    columns=["year", "fraction"],
)


# ---------------------------------------------------------------------------
# Core ECL primitive
# ---------------------------------------------------------------------------

def ecl_period_table(
    pds: Iterable[float],
    lgds: Iterable[float],
    eads: Iterable[float],
    eir: float,
    apply_pd_floor: bool = True,
) -> pd.DataFrame:
    """Return per-year ECL components: ECL_t = PD_t × LGD_t × EAD_t × DF_t.

    All vectors must be the same length. ``eir`` is the discount rate used
    to derive the discount factor DF_t = 1 / (1 + eir) ** t with t = 1..n.
    """

    pds = np.array(list(pds), dtype=float)
    lgds = np.array(list(lgds), dtype=float)
    eads = np.array(list(eads), dtype=float)
    if not (len(pds) == len(lgds) == len(eads)):
        raise ValueError("PD / LGD / EAD vectors must have equal length")

    if apply_pd_floor:
        pds = np.maximum(pds, PD_FLOOR_12M)

    t = np.arange(1, len(pds) + 1)
    df = 1.0 / (1.0 + eir) ** t
    period_ecl = pds * lgds * eads * df

    return pd.DataFrame(
        {
            "Year": t,
            "PD": pds,
            "LGD": lgds,
            "EAD (₹)": eads,
            "Discount Factor": df,
            "Period ECL (₹)": period_ecl,
        }
    )


def ecl_total(table: pd.DataFrame) -> float:
    return float(table["Period ECL (₹)"].sum())


# ---------------------------------------------------------------------------
# Probability-weighted scenarios (RBI requires unbiased estimate)
# ---------------------------------------------------------------------------

@dataclass
class Scenario:
    name: str
    pd_12m: float
    probability: float
    narrative: str = ""


def weighted_ecl(
    scenarios: list[Scenario],
    ead: float,
    lgd: float,
) -> pd.DataFrame:
    """Compute the probability-weighted Stage 1 ECL across macro scenarios.

    Probabilities should sum to ~1.0; the function does NOT auto-normalise so
    the user can see what they entered.
    """
    rows = []
    for s in scenarios:
        scenario_ecl = s.pd_12m * lgd * ead
        rows.append(
            {
                "Scenario": s.name,
                "Narrative": s.narrative,
                "12-mo PD": s.pd_12m,
                "Probability": s.probability,
                "Scenario ECL (₹)": scenario_ecl,
                "Weighted ECL (₹)": scenario_ecl * s.probability,
            }
        )
    df = pd.DataFrame(rows)
    return df


# ---------------------------------------------------------------------------
# Effective Interest Rate (EIR) — IRR on net cash flows
# ---------------------------------------------------------------------------

def derive_eir(cashflows: list[float], guess: float = 0.1) -> float:
    """Internal-rate-of-return solver. ``cashflows[0]`` is t=0 (negative for the
    bank since it's net amount disbursed). Subsequent entries are inflows.

    We use a robust Newton/secant fallback so we don't depend on numpy_financial
    being installed (it's optional in requirements).
    """
    cf = np.array(cashflows, dtype=float)

    def npv(rate: float) -> float:
        t = np.arange(len(cf))
        return float(np.sum(cf / (1.0 + rate) ** t))

    # bisection on a reasonable bracket
    low, high = -0.99, 5.0
    f_low, f_high = npv(low), npv(high)
    if f_low * f_high > 0:
        # try to widen the bracket
        for high_try in [10.0, 50.0, 200.0]:
            f_high = npv(high_try)
            if f_low * f_high < 0:
                high = high_try
                break
        else:
            # fall back to Newton
            r = guess
            for _ in range(200):
                f = npv(r)
                # numerical derivative
                dr = 1e-6
                fp = (npv(r + dr) - f) / dr
                if abs(fp) < 1e-12:
                    break
                r -= f / fp
                if abs(f) < 1e-9:
                    return r
            return r

    for _ in range(200):
        mid = 0.5 * (low + high)
        f_mid = npv(mid)
        if abs(f_mid) < 1e-9 or (high - low) < 1e-12:
            return mid
        if f_low * f_mid < 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
    return 0.5 * (low + high)


# ---------------------------------------------------------------------------
# Loan-level: amortisation schedule (equal annual principal + interest)
# ---------------------------------------------------------------------------

def equal_principal_schedule(
    principal: float,
    coupon: float,
    tenor: int,
    fee: float = 0.0,
) -> tuple[pd.DataFrame, list[float], float]:
    """Build a level-principal amortisation schedule.

    Returns (schedule, cashflows_for_eir, eir).
    cashflows_for_eir[0] = -(principal - fee), the rest are total inflows per year.
    """
    rows = [(0, "(Disbursal)", None, None, -(principal - fee), principal)]
    cashflows = [-(principal - fee)]
    outstanding = principal
    annual_principal = principal / tenor
    for year in range(1, tenor + 1):
        interest = outstanding * coupon
        cf = annual_principal + interest
        rows.append((year, outstanding, annual_principal, interest, cf, outstanding - annual_principal))
        cashflows.append(cf)
        outstanding -= annual_principal
    schedule = pd.DataFrame(
        rows,
        columns=["Year", "Opening Principal (₹)", "Principal Repaid (₹)",
                 "Interest @ coupon (₹)", "Total Cash Flow (₹)", "Closing Principal (₹)"],
    )
    eir = derive_eir(cashflows)
    return schedule, cashflows, eir


def amortised_cost_table(
    principal: float,
    coupon: float,
    tenor: int,
    fee: float,
    eir: float,
) -> pd.DataFrame:
    """Year-by-year amortised cost using EIR. Closing AC reaches ~0 at maturity."""
    annual_principal = principal / tenor
    rows = []
    ac = principal - fee
    outstanding = principal
    for year in range(1, tenor + 1):
        interest_eir = ac * eir
        cash = annual_principal + outstanding * coupon
        coupon_int = outstanding * coupon
        fee_amort = interest_eir - coupon_int
        ac_close = ac + interest_eir - cash
        rows.append((year, ac, interest_eir, cash, ac_close, coupon_int, fee_amort))
        ac = ac_close
        outstanding -= annual_principal
    return pd.DataFrame(
        rows,
        columns=["Year", "Opening AC (₹)", "Interest @ EIR (₹)", "Cash Inflow (₹)",
                 "Closing AC (₹)", "Coupon Interest (₹)", "Fee Amortisation (₹)"],
    )


# ---------------------------------------------------------------------------
# Floor application
# ---------------------------------------------------------------------------

def floor_for(category_code: str, stage: int) -> float | None:
    """Look up the Section N S1/S2 floor for a category code (e.g. '(ii)')."""
    row = S1_S2_FLOORS.loc[S1_S2_FLOORS["code"] == category_code]
    if row.empty:
        return None
    col = "stage1_floor" if stage == 1 else "stage2_floor"
    val = row.iloc[0][col]
    return None if pd.isna(val) else float(val)


def apply_portfolio_floor(
    portfolio: pd.DataFrame,
) -> pd.DataFrame:
    """Apply per-line MAX(model, floor) and produce a reported ECL column.

    Expected columns:
        category_code (str),  stage (int 1/2),  ead (float),
        floor_pct (float),  model_ecl (float)
    """
    df = portfolio.copy()
    df["Floor ECL (₹)"] = df["ead"] * df["floor_pct"]
    df["Reported ECL (₹)"] = np.maximum(df["model_ecl"], df["Floor ECL (₹)"])
    df["Floor Bound?"] = df["Reported ECL (₹)"] > df["model_ecl"] + 1e-6
    return df


def stage3_floor(
    secured_amt: float,
    unsecured_amt: float,
    bucket: str,
    table: pd.DataFrame,
) -> dict:
    """Compute Stage-3 individual-account floor."""
    row = table.loc[table["bucket"] == bucket]
    if row.empty:
        raise ValueError(f"Unknown bucket {bucket!r}")
    sec_pct = float(row.iloc[0]["secured"]) if not pd.isna(row.iloc[0]["secured"]) else 0.0
    unsec_pct = float(row.iloc[0]["unsecured"])
    sec_prov = secured_amt * sec_pct
    unsec_prov = unsecured_amt * unsec_pct
    total = sec_prov + unsec_prov
    ead = secured_amt + unsecured_amt
    return {
        "secured_pct": sec_pct,
        "unsecured_pct": unsec_pct,
        "secured_prov": sec_prov,
        "unsecured_prov": unsec_prov,
        "total_prov": total,
        "pct_of_ead": total / ead if ead else 0.0,
    }


# ---------------------------------------------------------------------------
# CET1 transitional add-back
# ---------------------------------------------------------------------------

def cet1_transition(
    ecl_apr_2027: float,
    irac_mar_2027: float,
    tax_rate: float = 0.252,
) -> pd.DataFrame:
    """Compute the four-year phased CET1 add-back per Section U."""
    gross = max(0.0, ecl_apr_2027 - irac_mar_2027)
    net = gross * (1 - tax_rate)
    rows = []
    for _, r in CET1_PHASE_IN.iterrows():
        f = float(r["fraction"])
        rows.append(
            {
                "Financial Year": r["year"],
                "Fraction (f)": f,
                "% Add-Back": f"{f*100:.0f}%",
                "Net Shortfall (₹ cr)": net,
                "CET1 Add-Back (₹ cr)": f * net,
                "P&L / RE Hit (₹ cr)": (1 - f) * net,
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Trade receivables — simplified approach (Annex 2)
# ---------------------------------------------------------------------------

def simplified_receivables_matrix(
    ageing: pd.DataFrame,
    base_rate: float = 0.005,
    forward_uplift: float = 1.10,
) -> pd.DataFrame:
    """Apply a provision matrix for trade / lease receivables.

    ``ageing`` must have columns: ['Bucket', 'Days Past Due', 'Outstanding (₹)'].
    The historical loss rate scales geometrically with the bucket index, then
    the forward-looking macro uplift multiplier is applied (per Annex 2).
    """
    df = ageing.copy()
    df["Historical Loss %"] = base_rate * (1.6 ** (df.index))
    df["Adj Loss %"] = df["Historical Loss %"] * forward_uplift
    df["ECL (₹)"] = df["Outstanding (₹)"] * df["Adj Loss %"]
    return df


# ---------------------------------------------------------------------------
# Convenience: P&L migration — origination → S1 → S2 → S3
# ---------------------------------------------------------------------------

def stage_migration_pnl(
    s1_ecl: float, s2_ecl: float, s3_ecl: float, tax_rate: float = 0.252
) -> pd.DataFrame:
    rows = [
        ("Origination → Stage 1",       s1_ecl, s1_ecl),
        ("Stage 1 → Stage 2 (SICR)",   s2_ecl, s2_ecl - s1_ecl),
        ("Stage 2 → Stage 3 (Default)", s3_ecl, s3_ecl - s2_ecl),
    ]
    out = []
    for label, reported, incremental in rows:
        tax = max(0.0, incremental) * tax_rate
        out.append(
            {
                "Migration": label,
                "Reported ECL (₹)": reported,
                "Incremental Provision (₹)": incremental,
                "Tax Shield (₹)": tax,
                "Net P&L Hit (₹)": incremental - tax,
            }
        )
    return pd.DataFrame(out)
