"""Page 3 — Interactive ECL = Σ PD × LGD × EAD × DF calculator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, style_fig, fmt_inr, fmt_pct, show_table, section, GOLD, LIGHTBLUE,
)

page_setup("ECL Calculator", icon="🧮")
hero(
    title="ECL Calculator — Σ PD × LGD × EAD × DF",
    subtitle="Build the loss expectation period-by-period and check the prudential floor on top.",
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

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
left, right = st.columns([1, 2])

with left:
    section("Loan inputs")
    ead = st.number_input("EAD — Exposure at Default (₹ cr)", min_value=0.1, value=10.0, step=0.5) * 1e7
    coupon_eir = st.number_input("EIR (decimal)", min_value=0.0, max_value=0.5, value=0.10, step=0.005, format="%.3f")
    lgd = st.slider("LGD (Loss Given Default)", 0.0, 1.0, 0.40, 0.01,
                    help="Bank's own estimate (RBI backstops: 65% secured / 70% unsecured; 30% for eligible collateral).")
    secured = st.checkbox("Secured exposure?", value=True)
    horizon = st.number_input("Lifetime horizon (years)", min_value=1, max_value=20, value=5)

    st.subheader("PD path")
    pd_mode = st.radio("How would you like to enter PDs?",
                       ["Single 12-month PD (Stage 1)", "Marginal PD per year (lifetime)"],
                       index=1)

    if pd_mode.startswith("Single"):
        pd_12m = st.slider("12-month PD", 0.0001, 0.20, 0.012, 0.001, format="%.4f")
        pds = [pd_12m]
        eads = [ead]
        lgds = [lgd]
        years_used = 1
    else:
        st.caption("Default values follow the workbook lifetime path. Override individual cells.")
        defaults = [0.04, 0.05, 0.04, 0.03, 0.025] + [0.02] * max(0, horizon - 5)
        defaults = defaults[:horizon]
        pds = []
        for i in range(horizon):
            pds.append(
                st.number_input(
                    f"Year {i+1} marginal PD", min_value=0.0, max_value=1.0,
                    value=float(defaults[i]), step=0.005, format="%.4f", key=f"pd_{i}"
                )
            )
        eads = [ead] * horizon
        lgds = [lgd] * horizon
        years_used = horizon

# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------
table = e.ecl_period_table(pds, lgds, eads, coupon_eir, apply_pd_floor=True)
total_ecl = e.ecl_total(table)

# Floor check
st.session_state.setdefault("category_choice", "(ii)")
with right:
    section("Floor check")
    cat = st.selectbox(
        "Loan category (Section N)",
        options=e.S1_S2_FLOORS["code"] + " — " + e.S1_S2_FLOORS["category"],
        index=1,
    )
    cat_code = cat.split(" — ")[0]
    stage_for_floor = 1 if pd_mode.startswith("Single") else 2
    floor_pct = e.floor_for(cat_code, stage_for_floor)
    floor_amt = (floor_pct or 0.0) * ead

    c1, c2, c3 = st.columns(3)
    c1.metric("Stage", f"Stage {stage_for_floor}")
    c2.metric("Floor %", "—" if floor_pct is None else fmt_pct(floor_pct, 3))
    c3.metric("Floor ECL", fmt_inr(floor_amt))

    reported = max(total_ecl, floor_amt)
    binding = "Yes — floor binds" if floor_amt > total_ecl else "No — model output binds"
    bcol1, bcol2, bcol3 = st.columns(3)
    bcol1.metric("Model ECL", fmt_inr(total_ecl))
    bcol2.metric("Reported ECL", fmt_inr(reported), delta=f"{(reported-total_ecl)/max(1,total_ecl)*100:+.1f}% vs model")
    bcol3.metric("Floor binding?", binding)

    section("Period-by-period table")
    show_table(table, {
        "PD": "{:.4f}",
        "LGD": "{:.2%}",
        "EAD (₹)": "{:,.0f}",
        "Discount Factor": "{:.4f}",
        "Period ECL (₹)": "{:,.0f}",
    })


# ---------------------------------------------------------------------------
# Visualisation: cumulative ECL build-up
# ---------------------------------------------------------------------------
section("How loss expectation accumulates over the horizon")
cum = table.copy()
cum["Cumulative ECL (₹)"] = cum["Period ECL (₹)"].cumsum()
fig = go.Figure()
fig.add_trace(go.Bar(
    x=cum["Year"], y=cum["Period ECL (₹)"], name="Period ECL",
    marker_color=COLORS["pine"],
    hovertemplate="Year %{x}<br>Period ECL = ₹%{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Scatter(
    x=cum["Year"], y=cum["Cumulative ECL (₹)"], name="Cumulative ECL",
    mode="lines+markers", line=dict(color=COLORS["gold"], width=3),
    marker=dict(size=10),
    hovertemplate="Year %{x}<br>Cumulative ECL = ₹%{y:,.0f}<extra></extra>",
))
fig.add_hline(y=floor_amt, line=dict(color=COLORS["ember"], dash="dash"),
              annotation_text=f"Floor ({fmt_inr(floor_amt)})", annotation_position="top right")
fig.update_layout(title="Period vs cumulative ECL", xaxis_title="Year", yaxis_title="₹",
                  height=420, hovermode="x unified")
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)

callout(
    f"<b>Reported ECL is always MAX(model, floor).</b> The floor is a regulatory backstop — not a cap. "
    f"In this configuration the {'<b>floor binds</b>' if floor_amt > total_ecl else '<b>model output binds</b>'} "
    f"and the bank reports <b>{fmt_inr(reported)}</b>.",
    kind="info" if floor_amt <= total_ecl else "warn",
)


# ---------------------------------------------------------------------------
# Pedagogy panel
# ---------------------------------------------------------------------------
with st.expander("📘 How this calculator works", expanded=False):
    st.markdown(
        r"""
        **Formula:** $\text{ECL} = \sum_t PD_t \times LGD_t \times EAD_t \times DF_t$

        - $T = 12\text{ months}$ for Stage 1, or remaining lifetime for Stages 2 & 3.
        - $DF_t = 1 / (1 + EIR)^t$ — discounting reflects the time-value of recoveries.
        - **PD floor:** the regulatory 12-month PD floor is **3 bps (0.03%)**.
        - **LGD backstops:** 65% secured / 70% unsecured. Eligible collateral (cash, gold, G-sec, LIC,
          KVP, NSC) caps LGD at **30%**.
        - **EAD:** banks may use opening principal or amortised cost. Credit-risk mitigants must NOT
          be netted from EAD.
        """
    )

footer()
