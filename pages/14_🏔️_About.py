"""Page 14 — About the project."""

from __future__ import annotations

import streamlit as st

from utils.theme import page_setup, hero, callout, footer, section, GOLD, LIGHTBLUE

page_setup("About", icon="🏔️")
hero(
    title="About this project",
    subtitle="A teaching companion for the RBI ECL Directions, 2026 — by The Mountain Path Academy.",
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


section("What this app is")
st.markdown(
    """
    A multi-page Streamlit application that walks practitioners through the RBI's expected-credit-loss
    framework end-to-end: framework, mechanics, prudential floors, transition arithmetic, and worked case
    studies. Every quantitative concept in the circular has a corresponding interactive calculator;
    every qualitative concept has structured notes with cross-references.

    The app is built around a **shared ECL engine** (``utils/ecl_engine.py``) so the same arithmetic
    powers the Loan Deep-Dive and the Bank-Wide Stress Test. Numbers were validated against the
    accompanying workbook *RBI_ECL_Directions_2026_Summary.xlsx*.
    """
)


section("Source")
st.markdown(
    """
    - **RBI Circular DOR.STR.REC.No.6/21.06.011/2026-27**, dated 27-Apr-2026.
    - Effective date for the framework: **1-Apr-2027**.
    - Companion workbook: ``RBI_ECL_Directions_2026_Summary.xlsx`` (12 sheets, each annotated).
    """
)


section("Module map")
st.markdown(
    """
    | Module | Purpose |
    | --- | --- |
    | 📜 Overview | Three pillars, key dates, applicability |
    | ⛰️ Stages & SICR | 3-stage model + DPD backstops + worked journey |
    | 🧮 ECL Calculator | Σ PD × LGD × EAD × DF with floor check |
    | 🌦️ Scenarios | Probability-weighted base / upside / downside |
    | 📐 Floors S1-S2 | All 15 product floors + portfolio calculator |
    | 📏 Floors S3 | Ageing-based progressive floors |
    | 🏛️ CET1 Transition | 4-year phased add-back simulator |
    | 🔁 IRAC vs ECL | Side-by-side dimension comparison |
    | 💰 Loan Deep-Dive | EIR, amortisation, ECL by stage, P&L waterfall |
    | 🧪 Case Studies | Six additional worked cases |
    | 📚 Detailed Notes | Searchable chapter notes |
    | 📖 Glossary | Every abbreviation in the circular |
    | 🪶 Exceptions | Special cases & decision tree |
    """
)


section("Built with")
st.markdown(
    "- **Python** + **Streamlit** for the UI\n"
    "- **pandas** + **numpy** for the data layer\n"
    "- **plotly** for the visualisations\n"
    "- A bespoke serif palette inspired by the Mountain Path Academy brand"
)


callout(
    "<b>Disclaimer.</b> This application is an educational illustration only. It is not investment, "
    "accounting, legal or regulatory advice. For implementation in a regulated bank, consult the "
    "circular text and the bank's accounting / risk committees.",
    kind="warn",
)


footer()
