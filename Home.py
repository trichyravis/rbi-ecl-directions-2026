"""RBI ECL Directions, 2026 — Mountain Path Academy.

Entry point for the multi-page Streamlit app. Run with:
    streamlit run Home.py
"""

from __future__ import annotations

import streamlit as st

from utils.theme import page_setup, hero, callout, footer, COLORS

page_setup("Home", icon="🏔️")

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
    st.markdown(f"### 🏔️ Mountain Path Academy")
    st.caption("Risk · Finance · Modelling")
    st.markdown("---")
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
# Hero metrics — the headline takeaways
# ----------------------------------------------------------------------------
st.subheader("The shift in one screen")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Effective Date", "1-Apr-2027", help="Entire loan portfolio fair-valued; opening ECL computed.")
with col2:
    st.metric("Loss Model", "Forward-looking", help="Replaces incurred-loss IRAC framework.")
with col3:
    st.metric("Stages", "3 + POCI", help="Stage 1 (12-mo ECL), Stage 2 (lifetime), Stage 3 (NPA / lifetime).")
with col4:
    st.metric("CET1 Phase-In", "4 years", help="80% → 60% → 40% → 20% add-back to opening CET1.")


# ----------------------------------------------------------------------------
# Three pillars
# ----------------------------------------------------------------------------
st.subheader("Three pillars of the framework")

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
st.subheader("Key dates")

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
    st.subheader("Applicability")
    st.markdown(
        "- **Applies to:** All Commercial Banks (including SBI, banking companies, "
        "corresponding new banks)\n"
        "- **Excluded:** Small Finance Banks (SFBs), Payment Banks, Local Area Banks (LABs), "
        "Regional Rural Banks (RRBs)"
    )
with right:
    st.subheader("Why this matters")
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

st.subheader("What this app contains")
st.markdown(
    """
    - **Interactive calculators** for every quantitative concept in the circular
      (PD × LGD × EAD, scenario weighting, EIR, CET1 transition).
    - **Reference tables** for all 15 Stage 1/2 product floors and all Stage 3 ageing buckets.
    - **A loan deep-dive** taking a single ₹100 cr loan from disbursal through SICR, default and cure.
    - **Six case studies** — retail unsecured, housing restructure, project-finance DCCO, wilful-defaulter
      / fraud overlays, trade-receivables simplified matrix, and a bank-level portfolio stress test.
    - **Detailed notes & glossary** for every chapter and every abbreviation.
    """
)

footer()
