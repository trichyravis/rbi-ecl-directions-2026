"""Page 5 — Stage 1 & Stage 2 prudential floors (Section N) + portfolio calculator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, style_fig, fmt_inr, fmt_pct, show_table,
)

page_setup("Floors — Stage 1 & 2", icon="📐")
hero(
    title="Prudential floors — Stage 1 & Stage 2 (Section N)",
    subtitle="Banks' own ECL estimates must be at least equal to these floors. Applied at the portfolio level per product category.",
)


# ---------------------------------------------------------------------------
# Reference table
# ---------------------------------------------------------------------------
st.subheader("All 15 categories")
disp = e.S1_S2_FLOORS.copy()
disp["Stage 1 floor"] = disp["stage1_floor"].apply(lambda x: fmt_pct(x, 3) if pd.notna(x) else "—")
disp["Stage 2 floor"] = disp["stage2_floor"].apply(
    lambda x: fmt_pct(x, 3) if pd.notna(x) else "DCCO-linked"
)
st.dataframe(
    disp[["code", "category", "Stage 1 floor", "Stage 2 floor"]]
        .rename(columns={"code": "#", "category": "Loan product category"}),
    use_container_width=True, hide_index=True,
)

callout(
    "<b>Three categories are DCCO-linked at Stage 2:</b> CRE-ADC (150% RW), CRE-RH-ADC and "
    "Project-finance pre-operational. The Stage 2 floor for these depends on whether the Date of "
    "Commencement of Commercial Operations (DCCO) has been deferred and by how much — see the "
    "circular for the slab schedule.",
    kind="info",
)


# ---------------------------------------------------------------------------
# Portfolio floor calculator
# ---------------------------------------------------------------------------
st.subheader("Portfolio-level floor application")
st.caption("Edit the rows below — the calculator returns reported ECL = MAX(model, floor) per line.")

default_portfolio = pd.DataFrame(
    [
        {"Category code": "(ii)",   "Stage": 1, "Portfolio EAD (₹ cr)": 5000, "Bank's model ECL (₹ cr)": 15.0},
        {"Category code": "(x)",    "Stage": 1, "Portfolio EAD (₹ cr)": 2000, "Bank's model ECL (₹ cr)": 15.0},
        {"Category code": "(xi-a)", "Stage": 2, "Portfolio EAD (₹ cr)": 800,  "Bank's model ECL (₹ cr)": 10.0},
        {"Category code": "(xiv)",  "Stage": 2, "Portfolio EAD (₹ cr)": 500,  "Bank's model ECL (₹ cr)": 35.0},
    ]
)

edited = st.data_editor(
    default_portfolio, hide_index=True, use_container_width=True, num_rows="dynamic",
    column_config={
        "Stage": st.column_config.SelectboxColumn(options=[1, 2]),
        "Portfolio EAD (₹ cr)": st.column_config.NumberColumn(format="%.2f", min_value=0.0),
        "Bank's model ECL (₹ cr)": st.column_config.NumberColumn(format="%.2f", min_value=0.0),
    },
)

# Compute --------------------------------------------------------------------
rows = []
for _, r in edited.iterrows():
    code = r["Category code"]
    stage = int(r["Stage"])
    ead_inr = float(r["Portfolio EAD (₹ cr)"]) * 1e7
    model_ecl = float(r["Bank's model ECL (₹ cr)"]) * 1e7
    floor_pct = e.floor_for(code, stage)
    if floor_pct is None:
        rows.append({
            "Category": code, "Stage": stage,
            "Portfolio EAD (₹ cr)": r["Portfolio EAD (₹ cr)"],
            "Floor %": "DCCO-linked",
            "Floor ECL (₹ cr)": np.nan,
            "Model ECL (₹ cr)": r["Bank's model ECL (₹ cr)"],
            "Reported ECL (₹ cr)": np.nan,
            "Floor binds?": "—",
        })
        continue
    floor_amt = ead_inr * floor_pct
    reported = max(model_ecl, floor_amt)
    rows.append({
        "Category": code, "Stage": stage,
        "Portfolio EAD (₹ cr)": r["Portfolio EAD (₹ cr)"],
        "Floor %": fmt_pct(floor_pct, 3),
        "Floor ECL (₹ cr)": floor_amt / 1e7,
        "Model ECL (₹ cr)": r["Bank's model ECL (₹ cr)"],
        "Reported ECL (₹ cr)": reported / 1e7,
        "Floor binds?": "Yes" if floor_amt > model_ecl else "No",
    })
result = pd.DataFrame(rows)
show_table(result, {
    "Portfolio EAD (₹ cr)": "{:,.2f}",
    "Floor ECL (₹ cr)":     "{:,.2f}",
    "Model ECL (₹ cr)":     "{:,.2f}",
    "Reported ECL (₹ cr)":  "{:,.2f}",
})

# Headline metrics
total_model = result["Model ECL (₹ cr)"].sum(skipna=True)
total_reported = result["Reported ECL (₹ cr)"].sum(skipna=True)
delta = total_reported - total_model
c1, c2, c3 = st.columns(3)
c1.metric("Total model ECL", f"₹{total_model:,.2f} cr")
c2.metric("Total reported ECL", f"₹{total_reported:,.2f} cr",
          delta=f"+₹{delta:,.2f} cr from floor")
c3.metric("% uplift from floors", f"{(delta/max(0.01,total_model))*100:+.1f}%")


# ---------------------------------------------------------------------------
# Visual: floors across all categories
# ---------------------------------------------------------------------------
st.subheader("Floors at a glance")
plot_df = e.S1_S2_FLOORS.copy()
plot_df["Stage 2 floor (visual)"] = plot_df["stage2_floor"].fillna(0.0)  # DCCO shown as 0 with note
plot_df["DCCO?"] = plot_df["stage2_floor"].isna()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=plot_df["category"], y=plot_df["stage1_floor"]*100,
    name="Stage 1 floor (%)", marker_color=COLORS["sage"],
    hovertemplate="%{x}<br>Stage 1 floor = %{y:.2f}%<extra></extra>",
))
fig.add_trace(go.Bar(
    x=plot_df["category"], y=plot_df["Stage 2 floor (visual)"]*100,
    name="Stage 2 floor (%)", marker_color=COLORS["gold"],
    text=plot_df["DCCO?"].map({True: "DCCO-linked", False: ""}),
    textposition="outside",
    hovertemplate="%{x}<br>Stage 2 floor = %{y:.2f}%<extra></extra>",
))
fig.update_layout(
    title="Stage 1 vs Stage 2 floors across all 15 categories",
    xaxis_tickangle=-35, height=520, barmode="group", yaxis_title="%",
)
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)

footer()
