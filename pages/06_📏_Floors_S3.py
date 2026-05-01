"""Page 6 — Stage 3 ageing-based prudential floors + interactive calculator."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, style_fig, fmt_inr, fmt_pct,
    section, GOLD, LIGHTBLUE,
)

page_setup("Floors — Stage 3", icon="📏")
hero(
    title="Stage 3 floors — applied at the individual account level",
    subtitle="Floors increase progressively with time in Stage 3. Three buckets cover the entire product universe.",
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
# Reference tables
# ---------------------------------------------------------------------------
def _show(table: pd.DataFrame, name: str):
    df = table.copy()
    if "secured" in df.columns:
        df["Secured"] = df["secured"].apply(lambda x: fmt_pct(x, 0) if pd.notna(x) else "—")
        df["Unsecured"] = df["unsecured"].apply(lambda x: fmt_pct(x, 0) if pd.notna(x) else "—")
        st.dataframe(df[["bucket", "Secured", "Unsecured"]].rename(columns={"bucket": "Duration in Stage 3"}),
                     use_container_width=True, hide_index=True)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

section("Table A — General categories (i)–(vi), (xii), (xiv), (xv)")
_show(e.S3_FLOORS_GENERAL, "general")

section("Table B — Lower-risk categories (vii)–(ix), (xi-a), (xiii)")
_show(e.S3_FLOORS_LOWER, "lower")

section("Table C — Unsecured retail (x)")
_show(e.S3_FLOORS_UNSECURED_RETAIL, "ur")


# ---------------------------------------------------------------------------
# Worked example
# ---------------------------------------------------------------------------
section("Worked example — single Stage-3 account")

c1, c2 = st.columns([1, 2])
with c1:
    secured = st.number_input("Secured portion (₹ cr)", min_value=0.0, value=6.0, step=0.5) * 1e7
    unsecured = st.number_input("Unsecured portion (₹ cr)", min_value=0.0, value=4.0, step=0.5) * 1e7
    bucket_choice = st.selectbox("Time in Stage 3", e.S3_FLOORS_GENERAL["bucket"].tolist())
    table_choice = st.radio("Floor table",
                            ["A — General", "B — Lower-risk", "C — Unsecured retail"],
                            index=0)

table_map = {
    "A — General":         e.S3_FLOORS_GENERAL,
    "B — Lower-risk":      e.S3_FLOORS_LOWER,
    "C — Unsecured retail": e.S3_FLOORS_UNSECURED_RETAIL,
}
chosen_table = table_map[table_choice]
# C uses different bucket labels — fall back to first if not found
if bucket_choice not in chosen_table["bucket"].values:
    bucket_choice = chosen_table["bucket"].iloc[0]

with c2:
    res = e.stage3_floor(secured, unsecured, bucket_choice, chosen_table)
    a, b, c = st.columns(3)
    a.metric("Secured floor %",   fmt_pct(res["secured_pct"]))
    b.metric("Unsecured floor %", fmt_pct(res["unsecured_pct"]))
    c.metric("Floor as % of EAD", fmt_pct(res["pct_of_ead"]))
    a.metric("Secured provision",   fmt_inr(res["secured_prov"]))
    b.metric("Unsecured provision", fmt_inr(res["unsecured_prov"]))
    c.metric("Total floor",         fmt_inr(res["total_prov"]))


# ---------------------------------------------------------------------------
# Progressive floor visual — same secured/unsecured split, every bucket
# ---------------------------------------------------------------------------
section("Progressive floor across buckets — same exposure, every duration")
rows = []
for bucket in chosen_table["bucket"]:
    r = e.stage3_floor(secured, unsecured, bucket, chosen_table)
    rows.append({"Bucket": bucket, "Total floor (₹)": r["total_prov"],
                 "Secured (₹)": r["secured_prov"], "Unsecured (₹)": r["unsecured_prov"]})
prog = pd.DataFrame(rows)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=prog["Bucket"], y=prog["Secured (₹)"], name="Secured",
    marker_color=COLORS["pine"],
    hovertemplate="%{x}<br>Secured = ₹%{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Bar(
    x=prog["Bucket"], y=prog["Unsecured (₹)"], name="Unsecured",
    marker_color=COLORS["ember"],
    hovertemplate="%{x}<br>Unsecured = ₹%{y:,.0f}<extra></extra>",
))
fig.update_layout(barmode="stack", title="Provision climbs with time in Stage 3",
                  xaxis_title="Time in Stage 3", yaxis_title="₹", height=420)
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)

callout(
    "<b>The Stage-3 floor is account-level (not portfolio-level).</b> Each NPA is provisioned "
    "separately, with the floor escalating as the account ages — this is the most punitive part of "
    "the framework and the strongest disincentive against allowing accounts to drift.",
    kind="warn",
)

footer()
