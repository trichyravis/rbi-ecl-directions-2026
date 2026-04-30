"""Page 9 — Single-loan deep dive: EIR, amortisation, ECL by stage, P&L."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import ecl_engine as e
from utils.theme import (
    page_setup, hero, callout, footer, COLORS, STAGE_COLORS, style_fig, fmt_inr, fmt_pct, show_table,
)

page_setup("Loan Deep-Dive", icon="💰")
hero(
    title="Single-loan deep dive — EIR, amortisation, ECL across stages",
    subtitle="Walks a hypothetical ₹100 cr corporate loan with an upfront fee through every step.",
)


# ---------------------------------------------------------------------------
# 1. Inputs
# ---------------------------------------------------------------------------
st.subheader("1 · Loan terms")
c1, c2, c3, c4 = st.columns(4)
principal = c1.number_input("Principal disbursed (₹ cr)", min_value=1.0, value=100.0, step=10.0) * 1e7
coupon = c2.number_input("Contractual coupon", min_value=0.0, max_value=0.4, value=0.10, step=0.005, format="%.3f")
tenor = c3.number_input("Tenor (years)", min_value=1, max_value=20, value=5)
fee = c4.number_input("Upfront fee (₹ cr)", min_value=0.0, value=2.0, step=0.5) * 1e7

c1, c2, c3 = st.columns(3)
lgd = c1.slider("LGD (secured)", 0.0, 1.0, 0.40, 0.01)
secured_share = c2.slider("Secured coverage at default", 0.0, 1.0, 0.70, 0.05)
tax = c3.slider("Tax rate", 0.0, 0.5, 0.252, 0.001, format="%.3f")


# ---------------------------------------------------------------------------
# 2. EIR derivation
# ---------------------------------------------------------------------------
schedule, cashflows, eir = e.equal_principal_schedule(principal, coupon, int(tenor), fee)

st.subheader("2 · EIR derivation")
st.caption("EIR is the rate that discounts the contractual cash flows back to the NET amount disbursed (= principal − upfront fee).")

c1, c2, c3 = st.columns(3)
c1.metric("Contractual coupon", fmt_pct(coupon, 3))
c2.metric("Effective Interest Rate", fmt_pct(eir, 4))
c3.metric("EIR uplift over coupon", f"+{(eir-coupon)*1e4:.1f} bps")

show_table(schedule, {c: "{:,.0f}" for c in schedule.columns if c != "Year"})

callout(
    f"The ₹{fee/1e7:.2f} cr upfront fee is **amortised through the EIR over the loan life** rather than "
    f"recognised at t=0. This is the central difference between EIR-based and contractual-rate "
    f"income recognition.",
    kind="info",
)


# ---------------------------------------------------------------------------
# 3. Amortised cost vs contractual
# ---------------------------------------------------------------------------
st.subheader("3 · Amortised cost using EIR (vs contractual coupon)")
ac = e.amortised_cost_table(principal, coupon, int(tenor), fee, eir)
show_table(ac, {c: "{:,.0f}" for c in ac.columns if c != "Year"})

# Visualise interest split
fig = go.Figure()
fig.add_trace(go.Bar(x=ac["Year"], y=ac["Coupon Interest (₹)"],
                     name="Coupon interest", marker_color=COLORS["pine"]))
fig.add_trace(go.Bar(x=ac["Year"], y=ac["Fee Amortisation (₹)"],
                     name="Fee amortisation", marker_color=COLORS["gold"]))
fig.update_layout(barmode="stack", title="Interest income split year-by-year",
                  xaxis_title="Year", yaxis_title="₹", height=380)
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# 4. ECL across stages
# ---------------------------------------------------------------------------
st.subheader("4 · ECL across the three stages")

# Use opening AC each year as EAD
eads = ac["Opening AC (₹)"].tolist()
marginal_pds = [0.012, 0.025, 0.03, 0.025, 0.02][:int(tenor)]
while len(marginal_pds) < int(tenor):
    marginal_pds.append(0.02)
lgds = [lgd] * int(tenor)

ecl_table = e.ecl_period_table(marginal_pds, lgds, eads, eir)

# Stage 1 = year 1 only ----------
s1_model = ecl_table.iloc[0]["Period ECL (₹)"]
s1_floor = principal * 0.004  # corporate Stage 1 floor 0.40%
s1 = max(s1_model, s1_floor)

# Stage 2 = sum across remaining lifetime
s2_model = ecl_table["Period ECL (₹)"].sum()
s2_floor = principal * 0.05
s2 = max(s2_model, s2_floor)

# Stage 3 — assume default at end of year 2 -----------
ac_at_default = float(ac.iloc[1]["Closing AC (₹)"])
secured_amt = ac_at_default * secured_share
unsecured_amt = ac_at_default * (1 - secured_share)
s3_floor_dict = e.stage3_floor(secured_amt, unsecured_amt, "0–1 year", e.S3_FLOORS_GENERAL)
bank_lifetime_loss = ac_at_default * (lgd * 0.85)  # illustrative bank model
s3 = max(s3_floor_dict["total_prov"], bank_lifetime_loss)

c1, c2, c3 = st.columns(3)
c1.metric("Stage 1 ECL (12-month)", fmt_inr(s1),
          delta=f"Floor binds" if s1 > s1_model + 1 else "Model binds")
c2.metric("Stage 2 ECL (lifetime)", fmt_inr(s2),
          delta=f"Floor binds" if s2 > s2_model + 1 else "Model binds")
c3.metric("Stage 3 ECL (NPA, 0–1 yr)", fmt_inr(s3),
          delta=f"Floor binds" if s3 > bank_lifetime_loss + 1 else "Model binds")

with st.expander("📑 Period-by-period ECL table (lifetime view)"):
    show_table(ecl_table, {
        "PD": "{:.4f}", "LGD": "{:.2%}",
        "EAD (₹)": "{:,.0f}",
        "Discount Factor": "{:.4f}",
        "Period ECL (₹)": "{:,.0f}",
    })


# ---------------------------------------------------------------------------
# 5. P&L migration impact
# ---------------------------------------------------------------------------
st.subheader("5 · P&L impact as the loan migrates")
pnl = e.stage_migration_pnl(s1, s2, s3, tax)
show_table(pnl, {c: "{:,.0f}" for c in pnl.columns if c != "Migration"})

# Waterfall
fig = go.Figure(go.Waterfall(
    x=pnl["Migration"].tolist() + ["Cumulative net hit"],
    measure=["relative", "relative", "relative", "total"],
    y=pnl["Net P&L Hit (₹)"].tolist() + [pnl["Net P&L Hit (₹)"].sum()],
    increasing={"marker": {"color": COLORS["ember"]}},
    totals={"marker": {"color": COLORS["pine"]}},
    text=[fmt_inr(v) for v in pnl["Net P&L Hit (₹)"].tolist() + [pnl["Net P&L Hit (₹)"].sum()]],
    textposition="outside",
))
fig.update_layout(title="Provision build as the loan deteriorates", height=440, yaxis_title="₹")
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# 6. Key takeaways
# ---------------------------------------------------------------------------
st.subheader("6 · Key takeaways")
st.markdown(
    f"""
    - **EIR ({fmt_pct(eir,4)})** > coupon ({fmt_pct(coupon,2)}) because the upfront fee is
      amortised across the loan life rather than booked Day 1.
    - **Day-1 Stage 1 ECL** is a NEW cost under the ECL framework — absent under IRAC. Even a healthy
      performing loan attracts a 12-month ECL provision.
    - **SICR triggers a JUMP from 12-month to lifetime ECL** — the largest single P&L hit in the loan's
      life if SICR occurs early.
    - **Stage 3 floors** apply at the INDIVIDUAL ACCOUNT level and increase progressively
      (25%/40% at 0–1 yr → 100%/100% after 4 yrs).
    - **Reported ECL is always MAX(bank model, RBI floor).** The floor is a regulatory backstop, not a
      cap.
    """
)

footer()
