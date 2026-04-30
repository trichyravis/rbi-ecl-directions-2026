"""Page 1 — Overview: framework, dates, applicability, expected impact."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.theme import page_setup, hero, callout, footer, COLORS, style_fig

page_setup("Overview", icon="📜")
hero(
    title="Overview — three pillars, key dates and what changes",
    subtitle=(
        "The 27-Apr-2026 circular is India's most significant shift in credit-risk provisioning since "
        "the 1992 prudential norms — a forward-looking expected-loss model layered on top of the "
        "retained 90-day NPA backstop."
    ),
)

# ---------------------------------------------------------------------------
# Pillars
# ---------------------------------------------------------------------------
st.subheader("Pillar 1 — ECL-based staging")
st.markdown(
    """
    The 3-stage ECL model replaces the **incurred-loss** approach. Each financial instrument is
    placed in one of three buckets:

    - **Stage 1 — Performing.** No significant increase in credit risk (SICR) since origination.
      Banks recognise a **12-month ECL** on the gross carrying amount.
    - **Stage 2 — Under-performing.** SICR has occurred; the asset is *not* yet credit-impaired.
      Banks recognise **lifetime ECL**.
    - **Stage 3 — Non-performing (NPA).** Default trigger satisfied. **Lifetime ECL** plus interest
      on a **cash basis**.

    The 90-day NPA norm is **retained** alongside, with stage transitions governed by both
    objective (DPD) and judgement-based (rating, covenants, watch-list, macro) signals.
    """
)

st.subheader("Pillar 2 — Forward-looking provisioning")
st.markdown(
    """
    ECL is the **probability-weighted** average of credit losses across multiple macroeconomic
    scenarios — minimum **base / upside / downside**. Probabilities are board-governed and derived
    from historical analysis + expert judgement. ECL must be **unbiased**: not the worst case,
    not the best case.
    """
)

st.subheader("Pillar 3 — EIR measurement at amortised cost")
st.markdown(
    """
    Income recognition moves from the **contractual rate** to the **Effective Interest Rate (EIR)**.
    EIR captures all integral upfront fees, transaction costs and discounts, and amortises them
    over the loan life. Existing loans may use the contractual rate during transition; full EIR
    migration is required by **31-Mar-2030**.
    """
)


# ---------------------------------------------------------------------------
# Timeline visual
# ---------------------------------------------------------------------------
st.subheader("Implementation timeline")

events = [
    ("2026-04-27", "Circular issued"),
    ("2027-04-01", "Framework live; opening ECL"),
    ("2027-06-30", "First quarterly ECL report"),
    ("2027-12-31", "Last parallel IRAC report"),
    ("2028-03-31", "First annual w/ comparatives"),
    ("2030-03-31", "Full EIR migration deadline"),
    ("2031-03-31", "End of CET1 transition"),
]
df = pd.DataFrame(events, columns=["date", "label"])
df["date"] = pd.to_datetime(df["date"])

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["date"], y=[0]*len(df),
        mode="markers+text",
        marker=dict(size=22, color=COLORS["pine"], line=dict(width=2, color=COLORS["snow"])),
        text=df["label"],
        textposition="top center",
        textfont=dict(family="Inter, serif", size=11),
        hovertemplate="%{text}<br>%{x|%d-%b-%Y}<extra></extra>",
    )
)
fig.update_yaxes(visible=False, range=[-1, 1.5])
fig.update_xaxes(showgrid=True, gridcolor="#E5DCC4")
fig.update_layout(height=260, showlegend=False, title="Five years of transition")
style_fig(fig)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Applicability + impact
# ---------------------------------------------------------------------------
left, right = st.columns(2)
with left:
    st.subheader("Applicability")
    st.markdown(
        """
        - **Applies to:** All Commercial Banks including SBI, banking companies, corresponding new banks.
        - **Excluded:** Small Finance Banks (SFBs), Payment Banks, Local Area Banks (LABs),
          Regional Rural Banks (RRBs).
        - **Scope of instruments:** loans, debt securities (non-FVTPL satisfying SPPI), trade and
          lease receivables, loan commitments (including undrawn) and off-balance-sheet credit
          exposures. Investments in subsidiaries / associates / JVs are excluded.
        """
    )

with right:
    st.subheader("Expected impact on bank financials")
    st.markdown(
        """
        - **Higher Day-1 provisioning** — Stage 1 ECL applies to the entire performing book (a new cost
          absent under IRAC).
        - **Earnings volatility** — forward-looking ECL fluctuates with macro forecasts, creating
          provisioning cyclicality.
        - **CET1 impact** — mitigated by the 4-year transitional add-back, but capital-thin banks face
          pressure.
        - **Pro-cyclicality** — downturns trigger mass Stage 1 → Stage 2 migrations, amplifying provision
          charges.
        - **Operational costs** — significant investment in data, models, validation and governance.
        """
    )

callout(
    "<b>Day-1 fair-valuation:</b> on 1-Apr-2027 the entire loan book is fair-valued. The difference "
    "vs carrying amount adjusts <b>opening retained earnings</b>, not P&L. Where fair value is not "
    "materially different from carrying amount, carrying amount is presumed to be best evidence of FV.",
    kind="info",
)

footer()
