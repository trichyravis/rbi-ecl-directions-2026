# RBI ECL Directions, 2026 — Streamlit teaching app

A multi-page Streamlit application that walks practitioners through the
**RBI Expected Credit Loss (ECL) Directions, 2026** end-to-end — framework,
mechanics, prudential floors, transition arithmetic and worked case studies.

Source: RBI Circular **DOR.STR.REC.No.6/21.06.011/2026-27** dated 27-Apr-2026 ·
effective 1-Apr-2027.

Built for **The Mountain Path Academy** in a serene serif palette (forest pine,
sage, warm parchment, slate) inspired by the academy's brand.

## Run locally

```bash
# 1. Install dependencies (Python 3.10+ recommended)
pip install -r requirements.txt

# 2. Launch the app
streamlit run Home.py
```

The app opens at <http://localhost:8501>. Use the page navigator in the left
sidebar to move between modules.

## Project layout

```
rbi_ecl_app/
├── Home.py                      # entry point — landing dashboard
├── pages/                       # one file per module (auto-discovered by Streamlit)
│   ├── 01_📜_Overview.py
│   ├── 02_⛰️_Stages_and_SICR.py
│   ├── 03_🧮_ECL_Calculator.py
│   ├── 04_🌦️_Scenarios.py
│   ├── 05_📐_Floors_S1_S2.py
│   ├── 06_📏_Floors_S3.py
│   ├── 07_🏛️_CET1_Transition.py
│   ├── 08_🔁_IRAC_vs_ECL.py
│   ├── 09_💰_Loan_Deep_Dive.py
│   ├── 10_🧪_Case_Studies.py     # six additional cases
│   ├── 11_📚_Detailed_Notes.py
│   ├── 12_📖_Glossary.py
│   ├── 13_🪶_Exceptions.py
│   └── 14_🏔️_About.py
├── utils/
│   ├── ecl_engine.py            # shared analytics — pure Python
│   └── theme.py                 # CSS + chart palette + helpers
├── .streamlit/
│   └── config.toml              # palette: pine/sage/parchment/slate
├── requirements.txt
└── README.md
```

## Modules at a glance

- **Overview** — three pillars, key dates, applicability, expected impact.
- **Stages & SICR** — the 3-stage model with a worked DPD trajectory and the
  30 / 60-day backstops.
- **ECL Calculator** — interactive Σ PD × LGD × EAD × DF with a floor check.
- **Scenarios** — probability-weighted base / upside / downside.
- **Floors S1-S2** — all 15 categories + portfolio-level calculator.
- **Floors S3** — Tables A / B / C with a progressive-ageing simulator.
- **CET1 Transition** — 4-year phased add-back simulator (80/60/40/20).
- **IRAC vs ECL** — side-by-side dimension comparison.
- **Loan Deep-Dive** — single ₹100 cr loan from EIR derivation through P&L.
- **Case Studies** — six new worked cases:
  1. Retail unsecured — Stage 1 → 3 walk
  2. Housing — restructure & SICR rebuttal
  3. Project finance — DCCO delay
  4. Wilful defaulter / fraud overlays
  5. Trade receivables — Annex 2 simplified matrix
  6. Bank-wide portfolio stress test
- **Detailed Notes** — searchable chapter-by-chapter notes.
- **Glossary** — every abbreviation in the circular.
- **Exceptions** — carve-outs & decision tree.
- **About** — credits, disclaimer, source.

## Numerical parity

All calculators are validated against the accompanying workbook
*RBI_ECL_Directions_2026_Summary.xlsx*. Key reference values:

| Input | Workbook | Engine |
| --- | ---: | ---: |
| Stage 1 ECL (12-mo, ₹10 cr corp.) | ₹4.36 lakh | ₹4.36 lakh |
| Lifetime ECL (Stage 2) | ₹57.50 lakh | ₹57.50 lakh |
| Probability-weighted ECL | ₹6.08 lakh | ₹6.08 lakh |
| EIR for ₹100 cr loan + ₹2 cr fee | 10.84% | 10.84% |
| CET1 add-back FY 2027–28 | ₹2,393.6 cr | ₹2,393.6 cr |

## Disclaimer

This application is an educational illustration only. It is **not** investment,
accounting, legal or regulatory advice. For implementation in a regulated bank,
consult the circular text and the bank's accounting / risk committees.
