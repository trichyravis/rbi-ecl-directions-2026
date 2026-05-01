"""RBI ECL Directions, 2026 — Mountain Path Academy.

Entry point for the multi-page Streamlit app. Run with:
    streamlit run Home.py
"""

from __future__ import annotations

import streamlit as st

from utils.theme import (
    page_setup, brand_banner, hero, callout, footer, section,
    stat_chip_row, defn_box, COLORS, GOLD, DARKBLUE, LIGHTBLUE,
)

page_setup("Home", icon="🏔️")

# Brand banner at top
brand_banner()

hero(
    title="RBI ECL Directions, 2026 — A Practitioner's Guide",
    subtitle=(
        "A complete walkthrough of India's shift to expected-credit-loss provisioning — "
        "framework, mechanics, prudential floors, transition arithmetic and worked case studies."
    ),
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
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
    st.markdown("")
    st.markdown("**Use the page navigator above** to jump between modules. Suggested order:")
    st.markdown(
        "1. Overview & Three Pillars\n"
        "2. Stages & SICR\n"
        "3. ECL Calculator\n"
        "4. Probability-Weighted Scenarios\n"
        "5. Floors (S1-S2 / S3)\n"
        "6. CET1 Transition\n"
        "7. IRAC vs ECL\n"
        "8. Loan Deep-Dive\n"
        "9. Case Studies\n"
        "10. Detailed Notes & Glossary"
    )
    st.markdown("---")
    st.caption("RBI Circular DOR.STR.REC.No.6/21.06.011/2026-27 · Issued 27-Apr-2026 · Effective 1-Apr-2027")


# ----------------------------------------------------------------------------
# Hero metrics — stat chips
# ----------------------------------------------------------------------------
section("The shift in one screen")

stat_chip_row([
    ("Effective Date", "1-Apr-2027"),
    ("Loss Model", "Forward-looking"),
    ("Stages", "3 + POCI"),
    ("CET1 Phase-In", "4 years"),
])

st.markdown("")

# ----------------------------------------------------------------------------
# Three pillars
# ----------------------------------------------------------------------------
section("Three pillars of the framework")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f"""
        <div class="mp-card">
            <div class="label">Pillar 1</div>
            <h3>ECL-based staging</h3>
            <p>Forward-looking <b>3-stage model</b> (Stage 1 / 2 / 3) replaces the incurred-loss approach.
            The 90-day NPA norm is <b>retained</b> alongside.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="mp-card">
            <div class="label">Pillar 2</div>
            <h3>Forward-looking provisioning</h3>
            <p><b>Macroeconomic forecasts</b>, probability-weighted scenarios, point-in-time risk parameters.
            ECL must be <i>unbiased</i> — neither worst-case nor best-case.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="mp-card">
            <div class="label">Pillar 3</div>
            <h3>EIR measurement</h3>
            <p><b>Effective Interest Rate</b> drives amortised-cost income recognition,
            replacing simple contractual rate accounting.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Key dates
# ----------------------------------------------------------------------------
section("Key dates")

import pandas as pd
dates = pd.DataFrame(
    [
        ("27-Apr-2026", "Circular issued"),
        ("1-Apr-2027", "ECL framework effective; entire loan portfolio fair-valued; opening ECL computed"),
        ("30-Jun-2027", "First quarterly reporting under ECL"),
        ("31-Dec-2027", "Last date for parallel IRAC reporting"),
        ("31-Mar-2028", "First annual reporting with prior-year comparatives"),
        ("31-Mar-2030", "Deadline for full EIR migration of all outstanding loans"),
        ("31-Mar-2031", "End of CET1 transitional adjustment period"),
    ],
    columns=["Date", "Milestone"],
)
st.dataframe(dates, use_container_width=True, hide_index=True)


# ----------------------------------------------------------------------------
# Applicability & call-outs
# ----------------------------------------------------------------------------
left, right = st.columns([1, 1])
with left:
    section("Applicability")
    defn_box(
        "SCOPE",
        "<b>Applies to:</b> All Commercial Banks (including SBI, banking companies, "
        "corresponding new banks)<br><br>"
        "<b>Excluded:</b> Small Finance Banks (SFBs), Payment Banks, Local Area Banks (LABs), "
        "Regional Rural Banks (RRBs)"
    )
with right:
    section("Why this matters")
    callout(
        "<b>Day-1 Stage 1 ECL</b> is a new cost on the entire performing book. "
        "Even healthy loans now attract a 12-month ECL provision — the largest behavioural change "
        "for Indian commercial banks since the 1992 prudential norms.",
        kind="info",
    )
    callout(
        "<b>Reported ECL = MAX(bank's model, RBI floor).</b> The floor is a regulatory backstop, "
        "not a cap. Optimisation cannot fall below it.",
        kind="warn",
    )

section("What this app contains")
defn_box(
    "MODULES",
    "<b>Interactive calculators</b> for every quantitative concept in the circular "
    "(PD x LGD x EAD, scenario weighting, EIR, CET1 transition).<br>"
    "<b>Reference tables</b> for all 15 Stage 1/2 product floors and all Stage 3 ageing buckets.<br>"
    "<b>Loan deep-dive</b> taking a single &#8377;100 cr loan from disbursal through SICR, default and cure.<br>"
    "<b>Six case studies</b> — retail unsecured, housing restructure, project-finance DCCO, wilful-defaulter "
    "/ fraud overlays, trade-receivables simplified matrix, and a bank-level portfolio stress test.<br>"
    "<b>Detailed notes &amp; glossary</b> for every chapter and every abbreviation."
)

footer()
