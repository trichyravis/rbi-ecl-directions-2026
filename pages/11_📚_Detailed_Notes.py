"""Page 11 — Detailed chapter-by-chapter notes from the RBI circular."""

from __future__ import annotations

import streamlit as st

from utils.theme import page_setup, hero, callout, footer

page_setup("Detailed Notes", icon="📚")
hero(
    title="Detailed notes — chapter by chapter",
    subtitle="Comprehensive reference notes for the RBI ECL Directions, 2026 — searchable by section.",
)

# Search box -----------------------------------------------------------------
query = st.text_input("🔍 Search notes (case-insensitive)", "")

NOTES = [
    ("1 · Executive overview", """
On 27-Apr-2026 the Reserve Bank of India (RBI) issued a landmark direction mandating all commercial banks
to adopt the Expected Credit Loss (ECL) framework for provisioning, effective 1-Apr-2027. This is India's
most significant shift in credit-risk provisioning since the introduction of prudential norms in 1992 and
aligns Indian banking with International Financial Reporting Standard 9 (IFRS 9) principles while
retaining India-specific safeguards (notably the 90-day Non-Performing Asset / NPA norm).

**Three pillars:** (1) ECL-based 3-stage staging framework replacing incurred-loss; (2) Forward-looking
provisioning with macroeconomic scenarios; (3) Effective Interest Rate (EIR) measurement at amortised
cost.

**Applies to** all Commercial Banks including State Bank of India (SBI). Excludes Small Finance Banks
(SFBs), Payment Banks, Local Area Banks (LABs) and Regional Rural Banks (RRBs). SFBs are referenced only
in the MSME exposure context.
"""),
    ("2 · NPA classification (Chapter II) — retained", """
The 90-day Non-Performing Asset (NPA) norm is **RETAINED**. ECL staging operates **alongside** NPA
classification, not in replacement. Stage 3 under ECL = NPA / credit-impaired.

**NPA triggers** (any one):
- Interest / principal overdue > 90 days for term loans / bills purchased & discounted.
- "Out of order" status for Overdraft (OD) / Cash Credit (CC) accounts for 90 days.
- OD/CC drawings on stock or receivable statements older than 3 months, permitted for 90 continuous days.
- Two crop seasons overdue (short-duration crops) or one crop season (long-duration crops) for
  agricultural loans.
- Liquidity facility outstanding > 90 days in securitisation.
- Partial Credit Enhancement (PCE) outstanding ≥ 90 days.
- Credit card minimum amount due unpaid for 90 days.
- Debt-instrument interest / instalment unpaid > 90 days.

**Borrower-level NPA:** if any one exposure to a borrower becomes NPA, ALL exposures to that borrower
must be classified as NPA. Upgrade requires repayment of entire arrears across all facilities.

**Sub-categories:** Sub-standard (NPA ≤ 12 months) → Doubtful (sub-standard for 12 months) → Loss
(uncollectible).

**Special exceptions:**
- Bills under Letter of Credit (LC) — not NPA unless LC documents are dishonoured and the borrower
  fails to make good.
- Advances against term deposits exempt if margin ≥ 100% (except where NPA arises from borrower-level
  tagging).
- Central Government guarantees — NPA only on repudiation.
- Co-Lending Arrangements (CLAs): borrower-level classification applies to both Regulated Entities (REs);
  information-sharing must occur by end of next working day.
"""),
    ("3 · The ECL framework (Chapter III)", """
**Scope:** loans, debt securities (non-FVTPL satisfying SPPI criterion), trade receivables, lease
receivables, loan commitments (including undrawn), off-balance-sheet credit exposures, and any other
financial asset with contractual cash-flow rights. Excludes investments in subsidiaries, associates and
joint ventures.

**Three stages:**
- **Stage 1** — no SICR since origination (low-credit-risk instruments also qualify) — 12-month ECL,
  facility level.
- **Stage 2** — SICR has occurred but the asset is NOT credit-impaired — lifetime ECL, facility level.
- **Stage 3** — credit-impaired (= NPA) — lifetime ECL, **borrower level**, interest recognised on cash
  basis only.

**SICR rebuttable presumptions / backstops:**
- > 30 DPD for term and amortising facilities.
- Outstanding above sanctioned limit / Drawing Power continuously for up to 60 days for revolving
  facilities (CC / OD).
- Rebuttal needs reasonable & supportable information, must not be routine or mechanical, and requires
  a Board-approved policy applied consistently.

**SICR parameters (Annex 1, illustrative):** internal/external rating downgrades, credit-spread changes,
CDS prices, adverse macroeconomic outlook, borrower financial distress, collateral-value deterioration,
covenant breaches, watch-list classification, past-due information.

**SICR exemptions:** SLR-eligible investments, direct claims on Central Government, exposures fully
guaranteed by Central Government, exposures to foreign sovereigns / central banks / MDBs / BIS / IMF
attracting 0% risk weight.

**Levels:** Stage 3 at BORROWER level (any exposure Stage 3 ⇒ all exposures Stage 3, including
non-funded). Stage 2 at FACILITY level.
"""),
    ("4 · ECL computation mechanics", """
**Formula:** $ECL = \\Sigma\\, PD_t \\times LGD_t \\times EAD_t \\times DF_t$

- T = 12 months for Stage 1 or remaining lifetime for Stage 2 / 3.
- ECL is the probability-weighted average across multiple macroeconomic scenarios.

**PD:** Stage 1 — 12-month PD; Stage 2 — lifetime PD (must reflect higher risk; not mechanically
derived from Stage 1 PD). Regulatory PD floor = 0.03% (12-month). Must incorporate forward-looking
macro variables; historical Observed Default Rate (ODR) adjusted for current conditions.

**LGD:** Bank's own estimate preferred (based on historical data). Regulatory backstop — secured 65%,
unsecured 70%. Specific eligible-collateral LGD = 30% (cash, gold including bullion & jewellery,
Government securities, LIC policies, KVP, NSC).

**EAD:** Bank-estimated. Credit-risk mitigants shall **NOT** be netted from EAD. For off-balance-sheet
items, regulatory Credit Conversion Factor (CCF) from the capital-charge directions may be used if
internal estimation is not reliable.

**Probability-weighted scenarios:** ECL must be unbiased — NOT worst-case, NOT best-case. Banks must use
multiple macroeconomic scenarios (minimum: base, upside, downside).

**EIR:** New loans (post 1-Apr-2027) — ECL discounted at EIR from inception. Existing loans — may use
contractual rate initially; full EIR migration by 31-Mar-2030. EIR includes all contractual terms,
integral fees, and transaction costs. Re-estimated for floating-rate instruments on benchmark changes.
POCI assets use Credit-Adjusted EIR.

**Lifetime period:** term loans — maximum contractual including extensions; loans with undrawn
commitment — period of credit-risk exposure even beyond contractual; revolving facilities without
auto-renewal — contractual period (renewal date used only when substantive reassessment is demonstrated);
revolving with auto-renewal (e.g., credit cards) — based on historical default patterns, drawdown
behaviour, effectiveness of limit actions; guarantees — maximum contractual obligation period.
"""),
    ("5 · Prudential floors (Section N)", """
Banks' own ECL estimates must be **at LEAST equal** to RBI-prescribed product- and stage-wise floors.
Stage 1 & 2 floors apply on a **portfolio basis** (per product category). Stage 3 floors apply at the
**individual account level**.

Stage 1 / Stage 2 floors span 15 product categories (i)–(xv): from secured retail (0.40% / 5%) and
corporate (0.40% / 5%) through unsecured retail (1% / 5%), gold loans (0.40% / 1.5%), housing loans
(0.25% / 1.5%), CRE (1.25% / DCCO-linked), to restructured-standard (5% / 10%) and residual
(0.40% / 5%). See the "Floors S1-S2" page for the full table.

**Stage 3 floors** increase progressively with time in Stage 3. Three buckets:
- **General categories:** 25 / 40 → 40 / 100 → 55 / 100 → 75 / 100 → 100 / 100 (sec / unsec %).
- **Lower-risk categories:** 10 / 25 → 20 / 100 → 30 / 100 → 40 / 100 → 100 / 100.
- **Unsecured retail:** 25% in year 1, 100% thereafter.
"""),
    ("6 · Income recognition (Chapter IV)", """
- **Stage 1 & 2:** interest recognised by applying EIR to GROSS carrying amount.
- **Stage 3 / credit-impaired:** interest NOT accrued — cash basis only.
- **POCI assets:** always cash basis.
- **On cure / upgrade from Stage 3:** revert to EIR on gross carrying amount, subject to staging and
  upgrade conditions.
- **Legacy pre-Apr-2027 loans:** may use contractual rate initially; must migrate to EIR by 31-Mar-2030.
"""),
    ("7 · Transition arrangements (Section U)", """
On 1-Apr-2027 banks must **fair-value** the entire loan portfolio. The difference between fair value
and carrying amount is adjusted against **opening retained earnings** (not P&L). Where fair value is
not materially different from carrying amount, carrying amount is presumed to be the best evidence of
fair value.

**CET1 capital transitional relief:** where ECL exceeds existing IRAC provisions, banks may add back a
declining post-tax fraction to CET1 — FY 2027–28: 4/5 (80%); FY 2028–29: 3/5 (60%); FY 2029–30: 2/5 (40%);
FY 2030–31: 1/5 (20%). The add-back flows to Tier 1 and Total Capital but **NOT** to Tier 2; cannot be
used to reduce SA exposure amounts or leverage-ratio exposure.

**Formula:** CET1 Add-Back = f × max(0, ECL on 1-Apr-2027 − IRAC provisions on 31-Mar-2027) × (1 − Tax
Rate), where f is the applicable phase-in fraction for the year.
"""),
    ("8 · Model risk management (Chapter V)", """
**Three-tier framework:**
- **Tier 1 — Front-line.** Model owners: develop, implement, use, validate.
- **Tier 2 — Risk Management & Compliance.** Oversight, validation, limits, remediation.
- **Tier 3 — Internal Audit.** Objective assurance on Tiers 1 & 2; reports to Board / Audit Committee.

**Six core principles:**
1. Comprehensive central model inventory with owners, tiering, dependencies and validation status.
2. Risk-based tiering — higher-impact models receive more frequent and rigorous validation.
3. Structured lifecycle: development → pre-implementation validation → implementation → monitoring →
   independent validation → recalibration / retirement.
4. Macroeconomic integration — multiple scenarios, probability-weighted, documented variable-selection
   rationale.
5. Post-Model Adjustments (PMAs) — management overlays must be documented with justification,
   calculation criteria and validation triggers.
6. Third-party models — banks remain fully responsible; contracts must enable RBI supervisory
   evaluation and access to documentation.
"""),
    ("9 · Governance framework", """
The Board of Directors has ultimate oversight of ECL implementation. A Board / Board-approved committee
(including the Chief Financial Officer / CFO and the Chief Risk Officer / CRO) must oversee ECL
strategy, methodology consistency, data integrity, governance over estimation, model-validation
independence, disclosure quality and regulatory compliance. Banks must ensure data granularity and
effective segmentation, and avoid grouping that masks individual-exposure deterioration. ECL estimates
must be unbiased with adequate processes, systems and controls.
"""),
    ("10 · Disclosures & reporting (Chapter VI)", """
**Annex 4 disclosure tables:**
- Table 1 — Credit quality of financial instruments — stage-wise with past-due ageing.
- Table 2 — Summary of loan assets, gross/net by stage.
- Table 3 — Loss-allowance reconciliation (opening to closing).
- Table 4 — PD / EAD / LGD methodology (quarterly to RBI).
- Table 5 — Macroeconomic assumptions — base / upside / downside (to RBI only).
- Table 6 — ECL adjustments — PMAs and overlays (to RBI only).
- Table 7 — Forward-looking PD / LGD by stage (to RBI only).
- Table 8 — SICR criteria by product category (to RBI only).
- Table 9 — Reconciliation of opening reserves (to RBI by 30-Jun-2027).
- Table 10 — Gross / Net advances and NPAs.

**Reporting timeline:** First ECL reporting based on financial position as on 30-Jun-2027. Parallel IRAC
reporting continues until 31-Dec-2027. Full prior-year comparatives begin from 31-Mar-2028.
"""),
    ("11 · Additional provisions & special cases", """
- **Stressed Assets Resolution:** additional provisioning per *Resolution of Stressed Assets Directions,
  2025*.
- **Fraud accounts:** full provisioning of amount due immediately on detection (less eligible financial
  collateral).
- **Foreign currency loans:** exchange-rate revaluation gains on FCY NPA loans must be used for
  additional provisioning.
- **Wilful defaulters:** additional 5% provision OVER ECL for exposures to companies with directors on
  the wilful-defaulter list.
- **Stage 3 collateral valuation:** for exposures > ₹7.5 cr, collateral valued at classification and at
  least every 2 years (stock: annually).
- **Default Loss Guarantee (DLG):** may be considered in ECL across all stages, provided the DLG is
  integral to loan terms and not separately recognised. ECL must be recomputed on each DLG invocation.
- **Floating / countercyclical provisions** may be utilised towards ECL provisioning.
- **ECL on investments:** same product-category floors apply based on issuer category. FVTPL
  non-performing instruments attract Stage 3 residual-category provisioning.
- **Simplified approach (Annex 2):** for trade and lease receivables — always lifetime ECL via provision
  matrix based on historical loss rates adjusted for forward-looking information.
"""),
    ("12 · IRAC vs ECL — key differences", """
- **Loss model:** incurred (backward-looking) → expected (forward-looking).
- **Trigger:** post-default → from Day 1.
- **Stages:** Standard / NPA → Stage 1 / 2 / 3 + POCI.
- **Standard provision:** flat 0.25–2% → model-based with floors.
- **Interest:** contractual rate → EIR.
- **Fair valuation:** not required → entire portfolio on 1-Apr-2027.
- **Macroeconomic inputs:** not formal → mandatory probability-weighted.
- **Governance:** not specifically prescribed → three-tier model-risk framework.
- **Capital impact:** direct P&L hit → 4-year transitional CET1 add-back.
"""),
    ("13 · Implications for Indian banks", """
**Action items:**
1. Build/procure PD–LGD–EAD models per portfolio segment with forward-looking macro variables.
2. Granular historical loss databases covering full business cycles.
3. Documented Board-approved SICR criteria and rebuttal policy.
4. Upgrade core banking systems for EIR computation and fee amortisation.
5. Methodologies for Day-1 fair valuation.
6. Quantify transitional adjustment and plan capital management across the 4-year phase-in.
7. Board-level ECL committee + three-tier model-risk framework.
8. Automated staging, provisioning, income recognition and audit trails per Annex 3.
"""),
]


def _matches(query: str, title: str, body: str) -> bool:
    if not query:
        return True
    q = query.lower()
    return q in title.lower() or q in body.lower()


hits = 0
for title, body in NOTES:
    if _matches(query, title, body):
        with st.expander(title, expanded=bool(query)):
            st.markdown(body)
        hits += 1

if query and hits == 0:
    callout(f"No matches for <b>{query!r}</b>. Try a different keyword.", kind="warn")

footer()
