"""Page 13 — Exceptions and special cases that override the standard ECL mechanics."""

from __future__ import annotations

import streamlit as st

from utils.theme import page_setup, hero, callout, footer, section, GOLD, LIGHTBLUE

page_setup("Exceptions", icon="🪶")
hero(
    title="Special cases & exceptions",
    subtitle=(
        "The standard ECL mechanics are subject to the following carve-outs. These exceptions "
        "may modify or override the standard result for specific exposures."
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

section("1 · NPA classification — exceptions (Chapter II)")
st.markdown(
    """
    - **Bills under Letter of Credit (LC):** Not classified as NPA even if other facilities of the
      borrower are NPA, **unless** LC documents are dishonoured and the borrower fails to make good.
    - **Advances against term deposits / LIC policies / KVP / NSC:** Exempt from NPA classification if
      margin **≥ 100%** is maintained (except where NPA arises from borrower-level tagging).
    - **Central Government guarantees:** Classified as NPA only when the government **repudiates** the
      guarantee.
    - **Co-Lending Arrangements (CLA):** Borrower-level classification applies — if either Regulated
      Entity (RE) classifies the borrower as Special Mention Account (SMA) / NPA, the same applies to
      the other RE's CLA exposure. Information sharing must occur by end of next working day.
    """
)

section("2 · SICR — exemptions (Chapter III)")
st.markdown(
    "The following instruments are NOT tested for SICR and do NOT require Stage 1 ECL:\n"
    "- Statutory Liquidity Ratio (SLR)-eligible investments\n"
    "- Direct claims on the Central Government\n"
    "- Exposures fully guaranteed by the Central Government\n"
    "- Exposures to foreign sovereigns / central banks / Multilateral Development Banks (MDBs) /\n"
    "  BIS / IMF attracting 0% risk weight"
)


section("3 · Additional provisions & special cases (Chapter VII)")
st.markdown(
    """
    - **Stressed Assets Resolution:** Additional provisioning per the *Resolution of Stressed Assets
      Directions, 2025* — over and above the ECL floors shown.
    - **Fraud accounts:** Full provisioning of the amount due **immediately** upon fraud detection
      (adjustable for eligible financial collateral) — supersedes the ageing-based Stage 3 floors.
    - **Foreign Currency NPAs:** Exchange-rate revaluation gains on NPA foreign currency loans must be
      channelled into additional provisioning (cannot be booked to P&L).
    - **Wilful Defaulters:** Additional **5% provision OVER and ABOVE** ECL for exposures to companies
      with directors on the wilful defaulter list.
    - **Stage 3 Collateral Valuation:** For exposures > **₹7.5 cr**, collateral must be valued at the
      time of classification and at least every 2 years (stock collateral: annually).
    - **Default Loss Guarantee (DLG):** May be considered in ECL across all stages, provided DLG is
      integral to loan terms and not separately recognised. ECL must be **recomputed** on each DLG
      invocation.
    - **Floating / countercyclical provisions:** May be utilised towards ECL provisioning.
    - **ECL on investments:** Same product-category floors apply based on issuer category. Fair Value
      Through Profit & Loss (FVTPL) non-performing instruments attract Stage 3 residual-category
      provisioning.
    - **Simplified Approach (Annex 2):** Available for trade and lease receivables — **always lifetime
      ECL** via a provision matrix based on historical loss rates adjusted for forward-looking
      information.
    - **POCI Assets:** Always recognise interest on cash basis; use Credit-Adjusted EIR.
    """
)


callout(
    "<b>Implication for portfolio modelling.</b> Special-case overlays sit on TOP of the standard "
    "ECL machinery — wilful-defaulter and fraud overlays apply regardless of stage. If a borrower "
    "in Stage 1 is later flagged as a wilful defaulter, the +5% kicks in on the existing ECL "
    "without re-staging.",
    kind="warn",
)

section("Decision tree — quick reference")
st.markdown(
    """
    ```
    Is the exposure a fraud account?  ────► YES ──► Provide 100% (less eligible collateral)
                                          │
                                          NO
                                          ▼
    Borrower in wilful-defaulter list?  ──► YES ──► Add +5% on top of ECL
                                          │
                                          NO
                                          ▼
    Stressed-asset resolution case?  ──► YES ──► Additional provisioning per Stressed Assets
                                          │
                                          NO
                                          ▼
    SICR exemption applies?  ──► YES ──► No Stage 1 ECL needed
                                          │
                                          NO
                                          ▼
                                       Apply standard ECL machinery
                                       (PD × LGD × EAD × DF, then floor check)
    ```
    """
)

footer()
