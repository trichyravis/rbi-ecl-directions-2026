"""Page 12 — Glossary of all abbreviations referenced in the directions."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.theme import page_setup, hero, footer, section, GOLD, LIGHTBLUE

page_setup("Glossary", icon="📖")
hero(
    title="Glossary — every abbreviation in the circular",
    subtitle="A reading aid for newcomers to the framework.",
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

GLOSSARY = pd.DataFrame(
    [
        ("ADC",   "Acquisition, Development & Construction (real-estate exposure type)"),
        ("BIS",   "Bank for International Settlements"),
        ("CC",    "Cash Credit (revolving credit facility)"),
        ("CCF",   "Credit Conversion Factor (off-balance-sheet to on-balance-sheet equivalent)"),
        ("CDS",   "Credit Default Swap"),
        ("CET1",  "Common Equity Tier 1 capital"),
        ("CFO",   "Chief Financial Officer"),
        ("CGTMSE","Credit Guarantee Fund Trust for Micro & Small Enterprises"),
        ("CLA",   "Co-Lending Arrangement"),
        ("CRE",   "Commercial Real Estate"),
        ("CRE-RH","Commercial Real Estate – Residential Housing"),
        ("CRO",   "Chief Risk Officer"),
        ("DCCO",  "Date of Commencement of Commercial Operations"),
        ("DF",    "Discount Factor (1 / (1 + EIR)^t)"),
        ("DLG",   "Default Loss Guarantee"),
        ("DP",    "Drawing Power (working-capital limit derived from collateral)"),
        ("DPD",   "Days Past Due"),
        ("EAD",   "Exposure at Default"),
        ("ECL",   "Expected Credit Loss"),
        ("EIR",   "Effective Interest Rate"),
        ("FCY",   "Foreign Currency"),
        ("FI",    "Financial Institution"),
        ("FVTPL", "Fair Value Through Profit & Loss"),
        ("GDP",   "Gross Domestic Product"),
        ("IFRS 9","International Financial Reporting Standard 9"),
        ("IMF",   "International Monetary Fund"),
        ("IRAC",  "Income Recognition, Asset Classification & Provisioning (the existing regime)"),
        ("KVP",   "Kisan Vikas Patra (small-savings instrument)"),
        ("LAB",   "Local Area Bank"),
        ("LC",    "Letter of Credit"),
        ("LGD",   "Loss Given Default"),
        ("LIC",   "Life Insurance Corporation of India"),
        ("MDB",   "Multilateral Development Bank"),
        ("MSME",  "Micro, Small & Medium Enterprises"),
        ("NBFC",  "Non-Banking Financial Company"),
        ("NPA",   "Non-Performing Asset"),
        ("NSC",   "National Savings Certificate"),
        ("OD",    "Overdraft (revolving facility)"),
        ("ODR",   "Observed Default Rate"),
        ("PCE",   "Partial Credit Enhancement"),
        ("PD",    "Probability of Default"),
        ("PMA",   "Post-Model Adjustment (management overlay on model output)"),
        ("POCI",  "Purchased or Originated Credit-Impaired"),
        ("P&L",   "Profit and Loss statement"),
        ("RBI",   "Reserve Bank of India"),
        ("RE",    "Regulated Entity"),
        ("RRB",   "Regional Rural Bank"),
        ("RW",    "Risk Weight"),
        ("SA",    "Standardised Approach (capital-charge methodology)"),
        ("SBI",   "State Bank of India"),
        ("SFB",   "Small Finance Bank"),
        ("SICR",  "Significant Increase in Credit Risk"),
        ("SLR",   "Statutory Liquidity Ratio"),
        ("SMA",   "Special Mention Account"),
        ("SPPI",  "Solely Payments of Principal & Interest"),
    ],
    columns=["Abbreviation", "Meaning"],
)

q = st.text_input("🔍 Filter glossary", "")
filtered = GLOSSARY
if q:
    mask = (
        GLOSSARY["Abbreviation"].str.contains(q, case=False, regex=False)
        | GLOSSARY["Meaning"].str.contains(q, case=False, regex=False)
    )
    filtered = GLOSSARY[mask]

st.dataframe(filtered.sort_values("Abbreviation").reset_index(drop=True),
             use_container_width=True, hide_index=True, height=620)

st.caption(f"{len(filtered)} of {len(GLOSSARY)} terms shown.")

footer()
