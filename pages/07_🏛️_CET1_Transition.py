"""Page 7 — CET1 transitional add-back simulator (Section U)."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, style_fig, fmt_inr, show_table,
    section, GOLD, LIGHTBLUE,
)

page_setup("CET1 Transition", icon="🏛️")
hero(
    title="CET1 transitional add-back — 4-year phased relief",
    subtitle=(
        "Where ECL on transition exceeds existing IRAC provisions, banks may add back a declining "
        "fraction of the post-tax shortfall to CET1 over four years."
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

section("Inputs")
c1, c2, c3 = st.columns(3)
with c1:
    ecl0 = st.number_input("ECL on 1-Apr-2027 (₹ cr)", min_value=0.0, value=12000.0, step=100.0)
with c2:
    irac0 = st.number_input("IRAC provisions on 31-Mar-2027 (₹ cr)", min_value=0.0, value=8000.0, step=100.0)
with c3:
    tax = st.slider("Tax rate", 0.0, 0.5, 0.252, 0.001, format="%.3f")

gross = max(0.0, ecl0 - irac0)
net = gross * (1 - tax)
table = e.cet1_transition(ecl0, irac0, tax)

c1, c2, c3 = st.columns(3)
c1.metric("Gross transitional shortfall", f"₹{gross:,.1f} cr")
c2.metric("Net (post-tax) shortfall",     f"₹{net:,.1f} cr")
c3.metric("Effective tax shield",         f"₹{gross-net:,.1f} cr")

section("Phased CET1 add-back")
show_table(table, {
    "Fraction (f)": "{:.2f}",
    "Net Shortfall (₹ cr)": "{:,.1f}",
    "CET1 Add-Back (₹ cr)": "{:,.1f}",
    "P&L / RE Hit (₹ cr)":  "{:,.1f}",
})


# ---------------------------------------------------------------------------
# Visual
# ---------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Bar(
    x=table["Financial Year"], y=table["CET1 Add-Back (₹ cr)"],
    name="CET1 add-back (capital relief)", marker_color=COLORS["pine"],
    hovertemplate="%{x}<br>Add-back = ₹%{y:,.1f} cr<extra></extra>",
))
fig.add_trace(go.Bar(
    x=table["Financial Year"], y=table["P&L / RE Hit (₹ cr)"],
    name="P&L / RE hit", marker_color=COLORS["ember"],
    hovertemplate="%{x}<br>Hit = ₹%{y:,.1f} cr<extra></extra>",
))
fig.update_layout(barmode="stack",
                  title=f"Phasing the ₹{net:,.0f} cr net shortfall over four years",
                  xaxis_title="Financial Year", yaxis_title="₹ cr", height=440)
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------
callout(
    "<b>Formula.</b> CET1 Add-Back = f × max(0, ECL₀ − IRAC₀) × (1 − Tax Rate), where f is the "
    "phase-in fraction for the year (4/5 → 3/5 → 2/5 → 1/5).",
    kind="info",
)

with st.expander("📘 Important fine print", expanded=False):
    st.markdown(
        """
        - The add-back flows to **Tier 1 and Total Capital** but **NOT to Tier 2**.
        - The add-back **shall not** be used to reduce Standardised Approach (SA) exposure amounts
          or leverage-ratio exposure.
        - The transitional shortfall is netted against **opening retained earnings**, not routed
          through P&L.
        - Where fair value is not materially different from carrying amount, carrying amount is
          presumed to be the best evidence of fair value on transition.
        - The relief is a **one-time** transitional measure and ends 31-Mar-2031.
        """
    )

footer()
