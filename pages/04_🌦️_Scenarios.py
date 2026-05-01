"""Page 4 — Probability-weighted macroeconomic scenarios."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, style_fig, fmt_inr, fmt_pct, show_table, section, GOLD, LIGHTBLUE,
)

page_setup("Scenarios", icon="🌦️")
hero(
    title="Probability-weighted macroeconomic scenarios",
    subtitle="ECL must be unbiased — neither worst-case nor best-case. Build base / upside / downside and weight them.",
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
# Inputs — common loan + scenarios
# ---------------------------------------------------------------------------
with st.sidebar:
    section("Common loan parameters")
    ead = st.number_input("EAD (₹ cr)", min_value=0.1, value=10.0, step=0.5) * 1e7
    lgd = st.slider("LGD", 0.0, 1.0, 0.40, 0.01)

section("Edit your scenarios")
default = pd.DataFrame(
    [
        {"Scenario": "Upside",   "Narrative": "GDP > 7%, low NPAs, easing rates",            "12-mo PD": 0.005, "Probability": 0.20},
        {"Scenario": "Base",     "Narrative": "GDP ~6.5%, stable inflation, baseline cycle",  "12-mo PD": 0.012, "Probability": 0.60},
        {"Scenario": "Downside", "Narrative": "Recession, GDP < 4%, rising NPAs, tightening", "12-mo PD": 0.035, "Probability": 0.20},
    ]
)
edited = st.data_editor(
    default, hide_index=True, use_container_width=True,
    num_rows="dynamic",
    column_config={
        "12-mo PD":   st.column_config.NumberColumn(format="%.4f", min_value=0.0, max_value=1.0),
        "Probability": st.column_config.NumberColumn(format="%.2f", min_value=0.0, max_value=1.0),
    },
)

# Validation -----------------------------------------------------------------
prob_sum = edited["Probability"].sum()
if abs(prob_sum - 1.0) > 1e-6:
    callout(
        f"<b>Probabilities sum to {prob_sum*100:.1f}% — they must sum to 100%.</b> "
        "Adjust the rows above before reading the results.",
        kind="warn",
    )

# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------
scenarios = [
    e.Scenario(name=row["Scenario"],
               pd_12m=float(row["12-mo PD"]),
               probability=float(row["Probability"]),
               narrative=row["Narrative"])
    for _, row in edited.iterrows()
]
res = e.weighted_ecl(scenarios, ead=ead, lgd=lgd)

# Single-PD comparison: what you'd get from base only
base_pd = float(edited.loc[edited["Scenario"].str.lower() == "base", "12-mo PD"].iloc[0]) if (edited["Scenario"].str.lower() == "base").any() else None
single_ecl = base_pd * lgd * ead if base_pd is not None else None
weighted_total = float(res["Weighted ECL (₹)"].sum())
delta = weighted_total - (single_ecl or 0)

col1, col2, col3 = st.columns(3)
col1.metric("Single base-PD ECL", fmt_inr(single_ecl) if single_ecl is not None else "—")
col2.metric("Probability-weighted ECL", fmt_inr(weighted_total))
col3.metric("Uplift from downside scenarios", fmt_inr(delta), delta=f"{delta/(single_ecl or 1)*100:+.1f}%")

show_table(res, {
    "12-mo PD": "{:.4f}",
    "Probability": "{:.2%}",
    "Scenario ECL (₹)": "{:,.0f}",
    "Weighted ECL (₹)": "{:,.0f}",
})


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
section("Scenario comparison charts")
left, right = st.columns(2)
with left:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=res["Scenario"], y=res["Scenario ECL (₹)"],
            name="Scenario ECL", marker_color=COLORS["pine"],
            hovertemplate="Scenario %{x}<br>ECL = ₹%{y:,.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=res["Scenario"], y=res["Weighted ECL (₹)"],
            name="Weighted ECL", marker_color=COLORS["gold"],
            hovertemplate="Scenario %{x}<br>Weighted ECL = ₹%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(barmode="group", title="Scenario vs weighted ECL", height=400)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = go.Figure(go.Pie(
        labels=res["Scenario"], values=res["Probability"],
        marker=dict(colors=[COLORS["sage"], COLORS["pine"], COLORS["ember"]] * 5),
        hole=0.5, textinfo="label+percent",
    ))
    fig.update_layout(title="Scenario probabilities", height=400, showlegend=False)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Pedagogy
# ---------------------------------------------------------------------------
callout(
    "<b>Why probability-weighting matters:</b> ECL is non-linear in PD. A small probability of a "
    "deep downturn can move the headline ECL meaningfully above the base-case-only number. "
    "RBI explicitly forbids using a single deterministic scenario.",
    kind="info",
)

with st.expander("📘 RBI requirements for scenario design", expanded=False):
    st.markdown(
        """
        - **Minimum three scenarios** (base / upside / downside) — banks may use more.
        - **Probabilities** derived from historical analysis + expert judgement, governed by the Board.
        - Each scenario links macro drivers (GDP, inflation, unemployment, exchange rate, sector indices)
          to PD / LGD / EAD parameters via documented relationships.
        - **Stress not pessimism** — the framework is unbiased; downside reflects plausible adverse paths,
          not the worst case.
        - **Variable selection** must be documented (Annex 3 governance requirements).
        - **Annual recalibration** at minimum, with quarterly monitoring of macro inputs.
        """
    )

footer()
