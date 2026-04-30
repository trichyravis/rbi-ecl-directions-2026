"""Page 8 — IRAC (old) vs ECL (new 2026) side-by-side comparison."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.theme import page_setup, hero, callout, footer

page_setup("IRAC vs ECL", icon="🔁")
hero(
    title="IRAC vs ECL — what changes, dimension by dimension",
    subtitle="A side-by-side reading of the old incurred-loss regime against the new expected-loss framework.",
)

table = pd.DataFrame(
    [
        ("Loss model",                 "Incurred loss (backward-looking)",                    "Expected loss (forward-looking)"),
        ("Provisioning trigger",       "After default (90 days overdue)",                     "From Day 1 (12-mo ECL on origination)"),
        ("Asset stages",               "Standard / NPA sub-categories",                       "Stage 1 / 2 / 3 + POCI"),
        ("Standard-asset provision",   "Flat percentage (0.25%–2%) by sector",                "Model-based ECL with product-wise floors"),
        ("NPA provisioning",           "Fixed percentages by NPA category",                   "ECL model output subject to progressive Stage 3 floors"),
        ("Interest rate basis",        "Contractual rate",                                    "Effective Interest Rate (EIR)"),
        ("Fair valuation",             "Not required at transition",                          "Entire portfolio fair-valued on 1-Apr-2027"),
        ("Macroeconomic inputs",       "Not formally required",                               "Mandatory — multiple scenarios, probability-weighted"),
        ("Model governance",           "Not specifically prescribed",                         "Three-tier model risk management + validation framework"),
        ("Capital impact",             "Direct P&L hit",                                      "Transitional CET1 add-back over 4 years"),
        ("Stage 3 / NPA level",        "Borrower-level",                                      "Borrower-level (retained); Stage 2 = facility-level"),
    ],
    columns=["Dimension", "Old IRAC regime", "New ECL framework (2026)"],
)
st.dataframe(table, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Expected impact
# ---------------------------------------------------------------------------
st.subheader("Expected impact on bank financials")
st.markdown(
    """
    - **Higher Day-1 provisioning:** Stage 1 ECL applies on the entire performing book — a new cost
      absent under IRAC.
    - **Earnings volatility:** forward-looking ECL fluctuates with macro forecasts, creating
      provisioning cyclicality.
    - **CET1 impact:** mitigated by the 4-year transitional relief, but capital-thin banks face pressure.
    - **Pro-cyclicality:** downturns trigger mass Stage 1 → Stage 2 migrations, amplifying provision
      charges.
    - **Operational costs:** significant investment in data, models, validation and governance
      infrastructure.
    """
)


# ---------------------------------------------------------------------------
# Special cases
# ---------------------------------------------------------------------------
st.subheader("Additional provisions & special cases")
st.markdown(
    """
    - **Stressed assets** — additional provisioning per the *Resolution of Stressed Assets Directions, 2025*.
    - **Fraud accounts** — full provisioning of the amount due immediately on detection
      (less eligible financial collateral).
    - **Wilful defaulters** — additional **5% provision OVER ECL** for exposures to companies with
      directors on the wilful-defaulter list.
    - **FX revaluation gains on FCY NPA loans** must be channelled into additional provisioning.
    - **Stage 3 collateral valuation** — for exposures > **₹7.5 cr**, valued at classification and at
      least every 2 years (stock collateral: annually).
    - **Trade & lease receivables** — simplified approach (Annex 2) — always lifetime ECL via
      provision matrix.
    """
)

callout(
    "<b>Net-net:</b> the ECL framework is more risk-sensitive but also more volatile. Banks that "
    "invest early in data, governance and model validation will absorb the transition more smoothly "
    "than those that defer.",
    kind="info",
)

footer()
