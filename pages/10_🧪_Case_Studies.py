"""Page 10 — Six additional case studies layered on top of the workbook content.

Tabs:
    1. Retail unsecured — Stage 1 → Stage 3 walk
    2. Housing loan — restructure + SICR rebuttal
    3. Project finance — DCCO delay
    4. Wilful defaulter & fraud overlays
    5. Trade receivables — simplified provision matrix (Annex 2)
    6. Bank-level portfolio stress test (mixed book, macro shock)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, STAGE_COLORS, style_fig, fmt_inr, fmt_pct, stage_chip, show_table,
    section, GOLD, LIGHTBLUE,
)

page_setup("Case Studies", icon="🧪")
hero(
    title="Case studies — six worked examples",
    subtitle=(
        "Layered scenarios that pick up where the base workbook leaves off — different products, "
        "special-case overlays and a bank-wide stress test."
    ),
)

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding:16px 0; border-bottom:2px solid {GOLD};">
            <div style="font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:900; color:{GOLD};">
                THE MOUNTAIN PATH
            </div>
            <div style="color:{LIGHTBLUE}; font-style:italic; font-size:0.85rem;">World of Finance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

tabs = st.tabs([
    "🧍 Retail Unsecured",
    "🏠 Housing — Restructure",
    "🏗️ Project Finance — DCCO",
    "⚠️ Wilful Defaulter / Fraud",
    "📦 Trade Receivables (Annex 2)",
    "🏦 Bank-Wide Stress Test",
])


# ---------------------------------------------------------------------------
# CASE 1 — Retail unsecured personal loan, Stage 1 → Stage 3 walk
# ---------------------------------------------------------------------------
with tabs[0]:
    section("Case 1 — Retail unsecured personal loan")
    st.caption("Demonstrates the **25% → 100%** floor escalation under Table C (Unsecured retail).")

    c1, c2, c3, c4 = st.columns(4)
    ead = c1.number_input("Outstanding (₹ lakh)", min_value=0.5, value=5.0, step=0.5, key="c1_ead") * 1e5
    coupon = c2.number_input("Effective rate", min_value=0.05, max_value=0.40, value=0.18, step=0.01, key="c1_rate")
    pd_12m = c3.slider("12-mo PD (Stage 1)", 0.001, 0.30, 0.06, 0.01, key="c1_pd")
    lgd = c4.slider("LGD", 0.3, 1.0, 0.70, 0.05, key="c1_lgd")  # unsecured backstop = 70%

    # Stage 1 — 12-mo ECL with model + floor (category x = 1.00%)
    s1_model = pd_12m * lgd * ead
    s1_floor = ead * 0.01
    s1 = max(s1_model, s1_floor)

    # Stage 2 — lifetime; assume 3-year remaining tenor, escalating PD
    horizon = 3
    pds_lifetime = [0.10, 0.12, 0.10]
    table = e.ecl_period_table(pds_lifetime, [lgd]*horizon, [ead]*horizon, coupon)
    s2_model = e.ecl_total(table)
    s2_floor = ead * 0.05
    s2 = max(s2_model, s2_floor)

    # Stage 3 walk — Table C: 25% in year 1 → 100% thereafter
    rows = []
    for bucket in ["0–1 year", "After 1 year"]:
        r = e.stage3_floor(0.0, ead, bucket, e.S3_FLOORS_UNSECURED_RETAIL)
        rows.append({"Bucket": bucket, "Floor %": fmt_pct(r["unsecured_pct"]),
                     "Floor provision (₹)": r["total_prov"]})
    s3_walk = pd.DataFrame(rows)

    c1, c2, c3 = st.columns(3)
    c1.metric("Stage 1 ECL", fmt_inr(s1),
              delta=("Floor binds" if s1_floor > s1_model else "Model binds"))
    c2.metric("Stage 2 ECL (lifetime)", fmt_inr(s2),
              delta=("Floor binds" if s2_floor > s2_model else "Model binds"))
    c3.metric("Stage 3 floor — Year 1", fmt_inr(s3_walk.iloc[0]["Floor provision (₹)"]))

    st.markdown("**Stage 3 progression (Table C — unsecured retail):**")
    show_table(s3_walk, {"Floor provision (₹)": "{:,.0f}"})

    callout(
        "<b>Why this case matters.</b> Unsecured retail has the steepest Stage-3 cliff in the framework: "
        "you go from a 25% floor in year one to a <b>full write-down</b> after 12 months in NPA. "
        "Combined with Stage-1 floor of 1% (the highest of any category), retail unsecured is the most "
        "expensive product to hold under the new regime.",
        kind="warn",
    )


# ---------------------------------------------------------------------------
# CASE 2 — Housing loan restructure + SICR rebuttal
# ---------------------------------------------------------------------------
with tabs[1]:
    section("Case 2 — Housing loan restructured into 'standard' bucket")
    st.caption("Shows the **5% Stage-1 / 10% Stage-2** floor for restructured-standard advances and the SICR rebuttal.")

    c1, c2, c3 = st.columns(3)
    ead = c1.number_input("Outstanding (₹ cr)", min_value=0.05, value=0.6, step=0.05, key="c2_ead") * 1e7
    months_in_restructure = c2.number_input("Months under restructure", min_value=1, max_value=120, value=18, key="c2_m")
    healthy_post = c3.checkbox("12 months sustained good performance after restructure?", value=True, key="c2_h")

    st.markdown("Two competing classifications:")
    a, b = st.columns(2)
    with a:
        st.markdown("**Option A — Treat as Restructured Standard (category xiv)**")
        s1_floor = ead * 0.05
        s2_floor = ead * 0.10
        st.markdown(f"- Stage 1 floor: **{fmt_inr(s1_floor)}** (5%)")
        st.markdown(f"- Stage 2 floor: **{fmt_inr(s2_floor)}** (10%)")
    with b:
        st.markdown("**Option B — Treat as Housing standard (category xi-a) post-cure**")
        s1_alt = ead * 0.0025
        s2_alt = ead * 0.015
        st.markdown(f"- Stage 1 floor: **{fmt_inr(s1_alt)}** (0.25%)")
        st.markdown(f"- Stage 2 floor: **{fmt_inr(s2_alt)}** (1.50%)")

    can_rebut = healthy_post and months_in_restructure >= 12
    callout(
        f"<b>SICR rebuttal:</b> {'allowed' if can_rebut else 'NOT allowed'} in this configuration. "
        "RBI permits the rebuttable presumption to be overturned only with reasonable & supportable "
        "information demonstrating the borrower no longer represents a SICR — typically a "
        "Board-approved minimum observation window after restructure (often 12 months of timely service). "
        "Even after rebuttal, the <b>Restructured-standard floor remains the higher of the two</b> until "
        "the account is permanently re-classified per Board policy.",
        kind="info" if can_rebut else "warn",
    )

    if can_rebut:
        st.success(
            f"After cure: bank may move from Option A to Option B — saving "
            f"~{fmt_inr(s1_floor-s1_alt)} on Stage-1 floor and {fmt_inr(s2_floor-s2_alt)} on Stage-2 "
            f"if SICR rebuttal is sustained."
        )


# ---------------------------------------------------------------------------
# CASE 3 — Project finance with DCCO delay
# ---------------------------------------------------------------------------
with tabs[2]:
    section("Case 3 — Project finance with DCCO delay")
    st.caption("Shows the **DCCO-linked Stage-2 floor** for pre-operational project-finance exposures.")

    c1, c2, c3 = st.columns(3)
    ead = c1.number_input("Sanctioned exposure (₹ cr)", min_value=10.0, value=500.0, step=50.0, key="c3_ead") * 1e7
    dcco_delay = c2.number_input("DCCO delay (months)", min_value=0, max_value=72, value=18, key="c3_d")
    operational = c3.checkbox("Project commercially operational?", value=False, key="c3_o")

    if operational:
        s1_floor = ead * 0.0040
        s2_floor = ead * 0.05
        cat = "(xii-b) Project finance — Operational"
    else:
        s1_floor = ead * 0.01
        # DCCO-linked Stage 2 — illustrative slab schedule (per public RBI commentary)
        if dcco_delay <= 6:    s2_pct = 0.05
        elif dcco_delay <= 12: s2_pct = 0.075
        elif dcco_delay <= 24: s2_pct = 0.10
        elif dcco_delay <= 36: s2_pct = 0.15
        else:                  s2_pct = 0.25
        s2_floor = ead * s2_pct
        cat = "(xii-a) Project finance — Pre-operational"

    c1, c2, c3 = st.columns(3)
    c1.metric("Category", cat.split(" — ")[0])
    c2.metric("Stage 1 floor", fmt_inr(s1_floor))
    c3.metric("Stage 2 floor",
              fmt_inr(s2_floor),
              delta=("DCCO-linked" if not operational else "Standard 5%"))

    if not operational:
        st.markdown("**Illustrative DCCO slab schedule (Stage 2):**")
        slab = pd.DataFrame(
            [
                ("0–6 months delay",   "5.0%"),
                ("6–12 months",         "7.5%"),
                ("12–24 months",       "10.0%"),
                ("24–36 months",       "15.0%"),
                ("> 36 months",        "25.0%"),
            ],
            columns=["DCCO delay", "Stage 2 floor"],
        )
        st.dataframe(slab, use_container_width=True, hide_index=True)
        callout(
            "<b>Why DCCO-linked floors exist:</b> projects that fail to commission on time tend to "
            "deteriorate sharply. The escalating slab structure forces banks to recognise this risk "
            "before formal SICR or default occurs.",
            kind="info",
        )


# ---------------------------------------------------------------------------
# CASE 4 — Wilful defaulter / fraud overlays
# ---------------------------------------------------------------------------
with tabs[3]:
    section("Case 4 — Wilful defaulter and fraud overlays")
    st.caption("Layer the special-case provisions on top of base ECL.")

    c1, c2, c3 = st.columns(3)
    ead = c1.number_input("Outstanding exposure (₹ cr)", min_value=1.0, value=50.0, step=5.0, key="c4_ead") * 1e7
    base_ecl_pct = c2.slider("Base ECL %", 0.0, 1.0, 0.25, 0.05, key="c4_pct")
    eligible_collateral = c3.number_input("Eligible financial collateral (₹ cr)", min_value=0.0, value=10.0, step=5.0, key="c4_col") * 1e7

    base_ecl = ead * base_ecl_pct

    # Wilful defaulter overlay = +5% over ECL
    wilful_overlay = ead * 0.05
    wilful_total = base_ecl + wilful_overlay

    # Fraud overlay = full provisioning (less eligible financial collateral)
    fraud_total = max(0.0, ead - eligible_collateral)

    cmp = pd.DataFrame(
        [
            {"Scenario": "Base ECL only",                 "Provision (₹)": base_ecl,
             "% of EAD": base_ecl/ead, "Notes": "Bank model + floor — no overlay"},
            {"Scenario": "Wilful defaulter (+5%)",       "Provision (₹)": wilful_total,
             "% of EAD": wilful_total/ead,
             "Notes": "Base ECL + 5% extra on EAD per circular"},
            {"Scenario": "Fraud account (immediate)",     "Provision (₹)": fraud_total,
             "% of EAD": fraud_total/ead,
             "Notes": "Full provisioning of amount due less eligible collateral"},
        ]
    )
    show_table(cmp, {"Provision (₹)": "{:,.0f}", "% of EAD": "{:.2%}"})

    fig = go.Figure(go.Bar(
        x=cmp["Scenario"], y=cmp["Provision (₹)"],
        marker_color=[COLORS["sage"], COLORS["gold"], COLORS["ember"]],
        text=[fmt_inr(v) for v in cmp["Provision (₹)"]], textposition="outside",
    ))
    fig.update_layout(title="Provision impact of the special-case overlays",
                      yaxis_title="₹", height=420)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    callout(
        "<b>Important.</b> Wilful-defaulter and fraud overlays apply <b>regardless of stage</b> — "
        "even on what the staging model would otherwise classify as Stage 1. They operate as "
        "punitive supplements, not substitutes, to the standard ECL machinery.",
        kind="warn",
    )


# ---------------------------------------------------------------------------
# CASE 5 — Trade receivables, simplified provision matrix (Annex 2)
# ---------------------------------------------------------------------------
with tabs[4]:
    section("Case 5 — Trade receivables under the simplified approach (Annex 2)")
    st.caption("Always lifetime ECL via a provision matrix — historical loss rate × forward-looking adjustment.")

    default_ageing = pd.DataFrame(
        [
            {"Bucket": "Current (0 dpd)", "Days Past Due": 0,    "Outstanding (₹)": 50_000_000},
            {"Bucket": "1–30 dpd",        "Days Past Due": 15,   "Outstanding (₹)": 12_000_000},
            {"Bucket": "31–60 dpd",       "Days Past Due": 45,   "Outstanding (₹)":  6_000_000},
            {"Bucket": "61–90 dpd",       "Days Past Due": 75,   "Outstanding (₹)":  3_000_000},
            {"Bucket": "> 90 dpd",        "Days Past Due": 120,  "Outstanding (₹)":  2_000_000},
        ]
    )
    edited = st.data_editor(default_ageing, hide_index=True, use_container_width=True)
    base_rate = st.slider("Historical loss rate (current bucket)", 0.001, 0.05, 0.005, 0.001, format="%.4f")
    uplift = st.slider("Forward-looking macro multiplier", 1.0, 3.0, 1.10, 0.05)

    res = e.simplified_receivables_matrix(edited, base_rate=base_rate, forward_uplift=uplift)
    show_table(res, {
        "Outstanding (₹)": "{:,.0f}",
        "Historical Loss %": "{:.2%}",
        "Adj Loss %": "{:.2%}",
        "ECL (₹)": "{:,.0f}",
    })
    total_o = res["Outstanding (₹)"].sum()
    total_e = res["ECL (₹)"].sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total receivables", fmt_inr(total_o))
    c2.metric("Lifetime ECL (matrix)", fmt_inr(total_e))
    c3.metric("Blended loss rate", fmt_pct(total_e/total_o))

    callout(
        "<b>Why a simplified approach exists.</b> Trade & lease receivables typically have short tenors "
        "and granular populations where building a full PD/LGD/EAD model is uneconomic. The matrix "
        "uses observed historical loss rates per ageing bucket, scaled by a forward-looking uplift "
        "(e.g. unemployment, sector indices). It is <b>always lifetime ECL</b> — there's no Stage 1 "
        "12-month variant.",
        kind="info",
    )


# ---------------------------------------------------------------------------
# CASE 6 — Bank-wide portfolio stress test
# ---------------------------------------------------------------------------
with tabs[5]:
    section("Case 6 — Bank-wide portfolio stress test")
    st.caption("Mixed book across categories. Apply a macro shock to PDs and watch the capital impact unfold.")

    # Default portfolio --------------------------------------------------------
    default_book = pd.DataFrame(
        [
            {"Category": "(ii) Corporate",          "EAD (₹ cr)": 50_000, "Stage": 1, "PD": 0.012, "LGD": 0.40},
            {"Category": "(ii) Corporate",          "EAD (₹ cr)":  4_000, "Stage": 2, "PD": 0.08,  "LGD": 0.40},
            {"Category": "(iii) SME",               "EAD (₹ cr)":  9_000, "Stage": 1, "PD": 0.020, "LGD": 0.45},
            {"Category": "(x) Unsecured retail",    "EAD (₹ cr)": 18_000, "Stage": 1, "PD": 0.060, "LGD": 0.70},
            {"Category": "(x) Unsecured retail",    "EAD (₹ cr)":  1_200, "Stage": 2, "PD": 0.18,  "LGD": 0.70},
            {"Category": "(xi-a) Housing",          "EAD (₹ cr)": 12_000, "Stage": 1, "PD": 0.008, "LGD": 0.30},
            {"Category": "(xiv) Restructured-std",  "EAD (₹ cr)":  1_500, "Stage": 2, "PD": 0.10,  "LGD": 0.50},
        ]
    )
    book = st.data_editor(default_book, hide_index=True, use_container_width=True, num_rows="dynamic")

    shock = st.slider("Downside macro shock — PD multiplier", 1.0, 4.0, 1.0, 0.1,
                      help="1.0 = base case; 2.0 doubles all PDs; 4.0 = severe recession.")

    floor_lookup = {
        "(ii) Corporate":         (0.0040, 0.05),
        "(iii) SME":              (0.0025, 0.05),
        "(x) Unsecured retail":   (0.0100, 0.05),
        "(xi-a) Housing":         (0.0025, 0.015),
        "(xiv) Restructured-std": (0.0500, 0.10),
    }

    rows = []
    for _, r in book.iterrows():
        ead = float(r["EAD (₹ cr)"]) * 1e7
        stage = int(r["Stage"])
        pd_ = float(r["PD"]) * shock
        lgd_ = float(r["LGD"])
        floor = floor_lookup.get(r["Category"], (0.004, 0.05))[stage-1]

        if stage == 1:
            model_ecl = pd_ * lgd_ * ead
        else:
            # rough lifetime: 5-year level PD path
            tab = e.ecl_period_table([pd_]*5, [lgd_]*5, [ead]*5, 0.10)
            model_ecl = e.ecl_total(tab)

        floor_amt = ead * floor
        reported = max(model_ecl, floor_amt)
        rows.append({
            "Category": r["Category"], "Stage": stage,
            "EAD (₹ cr)": r["EAD (₹ cr)"],
            "Model ECL (₹ cr)": model_ecl/1e7,
            "Floor ECL (₹ cr)": floor_amt/1e7,
            "Reported ECL (₹ cr)": reported/1e7,
        })
    res = pd.DataFrame(rows)

    show_table(res, {c: "{:,.2f}" for c in res.columns if c.endswith("(₹ cr)")})

    total_ead = res["EAD (₹ cr)"].sum()
    total_rep = res["Reported ECL (₹ cr)"].sum()
    blended = total_rep / total_ead if total_ead else 0.0
    capital_impact = total_rep * (1 - 0.252)  # post-tax hit to retained earnings

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total EAD", f"₹{total_ead:,.0f} cr")
    c2.metric("Total reported ECL", f"₹{total_rep:,.0f} cr")
    c3.metric("Blended ECL %", fmt_pct(blended))
    c4.metric("Net P&L / RE hit", f"₹{capital_impact:,.0f} cr",
              delta=f"after {25.2:.1f}% tax shield")

    # Stage breakdown chart ---------------------------------------------------
    by_stage = res.groupby("Stage", as_index=False)["Reported ECL (₹ cr)"].sum()
    fig = go.Figure(go.Bar(
        x=[f"Stage {s}" for s in by_stage["Stage"]],
        y=by_stage["Reported ECL (₹ cr)"],
        marker_color=[STAGE_COLORS[int(s)] for s in by_stage["Stage"]],
        text=[f"₹{v:,.0f} cr" for v in by_stage["Reported ECL (₹ cr)"]],
        textposition="outside",
    ))
    fig.update_layout(title="ECL by stage under the chosen shock",
                      yaxis_title="₹ cr", height=400)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    callout(
        f"<b>Reading the dashboard.</b> Even at a {shock:.1f}× macro shock, much of the Stage-1 book "
        "is still floor-bound — meaning the bank's ECL barely moves until SICR-driven Stage 2 "
        "migrations begin. That's the textbook pro-cyclicality concern: ECL stays stable, then "
        "lurches upward when a wave of accounts cross the SICR threshold. "
        "Move accounts from Stage 1 to Stage 2 in the table above to simulate that effect.",
        kind="warn",
    )

footer()
