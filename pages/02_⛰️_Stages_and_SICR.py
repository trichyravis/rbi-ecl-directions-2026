"""Page 2 — The 3-stage model + SICR triggers + a worked loan journey."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.theme import page_setup, hero, callout, footer, COLORS, STAGE_COLORS, stage_chip, style_fig

page_setup("Stages & SICR", icon="⛰️")
hero(
    title="The 3-stage model & Significant Increase in Credit Risk",
    subtitle="How a loan moves between Stage 1, Stage 2 and Stage 3 — triggers, backstops, cure conditions.",
)


# ---------------------------------------------------------------------------
# Stage definitions
# ---------------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
for col, stage, title, body in [
    (c1, 1, "Performing", "No SICR since origination. Low-credit-risk instruments also qualify."),
    (c2, 2, "Under-performing", "SICR has occurred but the asset is NOT credit-impaired."),
    (c3, 3, "Non-performing (NPA)", "Credit-impaired = NPA (90+ DPD or other default trigger)."),
]:
    with col:
        st.markdown(stage_chip(stage), unsafe_allow_html=True)
        st.markdown(f"#### {title}")
        st.markdown(body)
        st.markdown(
            f"- **ECL basis:** {'12-month ECL' if stage == 1 else 'Lifetime ECL'}\n"
            f"- **Interest:** {'Cash basis only' if stage == 3 else 'EIR × gross carrying amount'}\n"
            f"- **Level:** {'Borrower-level' if stage == 3 else 'Facility-level'}"
        )


# ---------------------------------------------------------------------------
# SICR rebuttable presumptions
# ---------------------------------------------------------------------------
st.subheader("SICR — rebuttable presumptions (the 30 / 60-day backstops)")

sicr = pd.DataFrame(
    [
        ("Term loans / amortising",
         "> 30 days past due",
         "Rebuttable with reasonable & supportable info; not mechanical."),
        ("Revolving — Cash Credit / Overdraft",
         "Outstanding > sanctioned limit / DP for up to 60 continuous days",
         "Rebuttal policy must be Board-approved and applied consistently."),
    ],
    columns=["Facility type", "DPD trigger", "Notes"],
)
st.dataframe(sicr, use_container_width=True, hide_index=True)

st.markdown("**Other SICR signals (Annex 1, illustrative):**")
st.markdown(
    "- Internal / external rating downgrades, credit-spread changes, CDS prices\n"
    "- Adverse macroeconomic outlook, borrower financial distress, covenant breaches\n"
    "- Collateral-value deterioration, watch-list classification, past-due information\n"
    "- All criteria must be **documented and used consistently**."
)

callout(
    "<b>SICR exemptions (no Stage 1 ECL):</b> SLR-eligible investments, direct claims on the Central "
    "Government, exposures fully guaranteed by the Central Government, and exposures to foreign "
    "sovereigns / central banks / MDBs / BIS / IMF attracting 0% risk weight.",
    kind="info",
)


# ---------------------------------------------------------------------------
# Worked loan journey
# ---------------------------------------------------------------------------
st.subheader("Worked example — loan journey through stages")
st.caption("Hypothetical ₹10 cr corporate term loan — 5 years, 10% coupon, secured.")

journey = pd.DataFrame(
    [
        ("2027-04-01", "Loan disbursed (₹10 cr corporate term loan)",       0,  1, "12-month ECL", "EIR × Gross"),
        ("2027-06-30", "First quarterly reporting",                          0,  1, "12-month ECL", "EIR × Gross"),
        ("2027-08-15", "Borrower misses instalment",                        35,  2, "Lifetime ECL", "EIR × Gross"),
        ("2027-11-20", "Default — 90+ DPD",                                 95,  3, "Lifetime ECL", "Cash basis only"),
        ("2028-04-10", "Borrower clears all arrears (cure)",                 0,  2, "Lifetime ECL", "EIR × Gross"),
        ("2028-10-10", "Sustained good performance — 6 months",              0,  1, "12-month ECL", "EIR × Gross"),
    ],
    columns=["Date", "Event", "DPD", "Stage", "ECL Basis", "Interest Income"],
)
journey["Date"] = pd.to_datetime(journey["Date"])
st.dataframe(journey.assign(Date=journey["Date"].dt.strftime("%d-%b-%Y")),
             use_container_width=True, hide_index=True)

# Visual stage timeline ----------------------------------------------------
fig = go.Figure()
for stage_no in [1, 2, 3]:
    sub = journey[journey["Stage"] == stage_no]
    fig.add_trace(
        go.Scatter(
            x=sub["Date"], y=sub["DPD"],
            mode="markers+lines",
            name=f"Stage {stage_no}",
            marker=dict(size=14, color=STAGE_COLORS[stage_no],
                        line=dict(width=2, color=COLORS["snow"])),
            line=dict(color=STAGE_COLORS[stage_no], width=2),
            hovertemplate="%{customdata}<br>%{x|%d-%b-%Y}<br>DPD = %{y}<extra></extra>",
            customdata=sub["Event"],
        )
    )
# horizontal lines for thresholds
fig.add_hline(y=30, line=dict(color=COLORS["gold"], dash="dot"),
              annotation_text="30 DPD — SICR backstop", annotation_position="top left")
fig.add_hline(y=90, line=dict(color=COLORS["ember"], dash="dot"),
              annotation_text="90 DPD — NPA backstop", annotation_position="top left")
fig.update_layout(title="DPD trajectory & stage migrations",
                  xaxis_title="", yaxis_title="Days past due",
                  height=420, hovermode="x unified")
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Cure conditions
# ---------------------------------------------------------------------------
st.subheader("Cure & upgrade conditions")
st.markdown(
    """
    - **Stage 3 → Stage 2:** Account becomes *standard* (entire arrears cleared across all facilities of
      the borrower). Borrower-level upgrade requirement remains intact.
    - **Stage 2 → Stage 1:** Sustained good performance per Board-approved upgrade policy
      (typically a defined observation window after SICR removal).
    - **Borrower-level NPA principle:** if any one exposure to a borrower becomes NPA, *all* exposures
      (including non-funded) are classified as NPA. Upgrade requires repayment of arrears across all
      facilities.
    """
)

callout(
    "<b>Symmetry:</b> upgrades are not automatic. SICR rebuttal and cure both require documented, "
    "Board-approved policies and reasonable & supportable information — no mechanical rules.",
    kind="info",
)

footer()
