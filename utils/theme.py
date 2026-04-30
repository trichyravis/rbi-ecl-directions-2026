"""Shared visual identity for the Mountain Path Academy — RBI ECL Directions app.

A small but consistent design system: colour tokens, typography, reusable CSS
injected once per page, plus helpers for cards, metric tiles, hero banners and
chart styling so every page feels like it belongs to the same publication.
"""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Colour tokens — kept in one place so charts and CSS stay in sync
# ---------------------------------------------------------------------------
COLORS = {
    "pine":     "#2F5D50",   # primary — deep mountain pine
    "moss":     "#5C8374",   # secondary green
    "sage":     "#9EC8B9",   # tertiary / accent green
    "parchment":"#FBF7EE",   # background
    "paper":    "#F1E8D6",   # secondary background
    "slate":    "#1F2A24",   # body text
    "stone":    "#6F6A5F",   # muted text / borders
    "ember":    "#B8552B",   # accent for warnings / regulatory floor breaches
    "gold":     "#C8A24B",   # accent for highlights, CET1, capital
    "snow":     "#FFFFFF",
}

STAGE_COLORS = {
    1: COLORS["sage"],
    2: COLORS["gold"],
    3: COLORS["ember"],
}

PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Georgia, 'Times New Roman', serif", "color": COLORS["slate"], "size": 13},
        "paper_bgcolor": COLORS["parchment"],
        "plot_bgcolor": COLORS["parchment"],
        "colorway": [COLORS["pine"], COLORS["moss"], COLORS["gold"], COLORS["ember"], COLORS["sage"], COLORS["stone"]],
        "xaxis": {"gridcolor": "#E5DCC4", "zerolinecolor": "#E5DCC4"},
        "yaxis": {"gridcolor": "#E5DCC4", "zerolinecolor": "#E5DCC4"},
        "legend": {"bgcolor": "rgba(0,0,0,0)"},
        "title": {"font": {"family": "'Playfair Display', Georgia, serif", "size": 18}},
        "margin": {"l": 60, "r": 30, "t": 60, "b": 50},
    }
}


def style_fig(fig):
    """Apply the Mountain Path template to a Plotly figure."""
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig


# ---------------------------------------------------------------------------
# Global CSS — one injection per page
# ---------------------------------------------------------------------------
_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', Georgia, serif;
    color: {COLORS['slate']};
}}

h1, h2, h3, h4 {{
    font-family: 'Playfair Display', Georgia, serif;
    color: {COLORS['pine']};
    letter-spacing: -0.01em;
}}

h1 {{ font-weight: 700; }}
h2 {{ border-bottom: 1px solid #E5DCC4; padding-bottom: 0.35rem; margin-top: 1.2rem; }}

/* sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLORS['paper']} 0%, {COLORS['parchment']} 100%);
    border-right: 1px solid #E5DCC4;
}}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: {COLORS['pine']};
}}

/* hero banner */
.hero {{
    background: linear-gradient(135deg, {COLORS['pine']} 0%, {COLORS['moss']} 60%, {COLORS['sage']} 100%);
    color: {COLORS['snow']};
    padding: 2.2rem 2rem 1.8rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 20px rgba(47, 93, 80, 0.15);
}}
.hero h1 {{
    color: {COLORS['snow']};
    margin: 0 0 0.4rem 0;
    font-size: 2.0rem;
    font-weight: 700;
}}
.hero .eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.72rem;
    opacity: 0.85;
    margin-bottom: 0.6rem;
}}
.hero p {{
    color: rgba(255,255,255,0.92);
    margin: 0;
    font-size: 1.02rem;
    max-width: 80ch;
}}

/* card */
.mp-card {{
    background: {COLORS['snow']};
    border: 1px solid #E5DCC4;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 4px rgba(31,42,36,0.04);
}}
.mp-card .label {{
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: {COLORS['stone']};
    font-size: 0.72rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}}
.mp-card h3 {{
    margin: 0 0 0.4rem 0;
    color: {COLORS['pine']};
    font-size: 1.05rem;
}}
.mp-card .value {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.6rem;
    color: {COLORS['pine']};
    font-weight: 700;
}}

/* stage chips */
.stage-chip {{
    display: inline-block;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}
.stage-1 {{ background: #DDEDE5; color: #2F5D50; }}
.stage-2 {{ background: #F4E2BE; color: #8B6A1E; }}
.stage-3 {{ background: #F4D6C5; color: #7B3416; }}

/* call-out boxes */
.callout {{
    border-left: 4px solid {COLORS['gold']};
    background: #FBF3DD;
    padding: 0.9rem 1.1rem;
    border-radius: 6px;
    margin: 0.8rem 0;
    color: {COLORS['slate']};
}}
.callout.warn  {{ border-left-color: {COLORS['ember']}; background: #FBE6DA; }}
.callout.info  {{ border-left-color: {COLORS['moss']};  background: #E7F0EB; }}
.callout strong {{ color: {COLORS['pine']}; }}

/* footer */
.mp-footer {{
    color: {COLORS['stone']};
    font-size: 0.78rem;
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #E5DCC4;
}}

/* tighten metric default */
[data-testid="stMetricValue"] {{
    font-family: 'Playfair Display', Georgia, serif;
    color: {COLORS['pine']};
}}

/* table polish */
.stDataFrame, .stTable {{
    border-radius: 8px;
    overflow: hidden;
}}

/* tab polish */
.stTabs [data-baseweb="tab-list"] button {{
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    color: {COLORS['pine']} !important;
    border-bottom-color: {COLORS['pine']} !important;
}}
</style>
"""


def apply_theme():
    """Inject the global CSS. Call at the top of every page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str, eyebrow: str = "RBI ECL Directions, 2026"):
    """A consistent banner for each page."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(label: str, title: str, value: str, body: str = ""):
    """A small content card with label / title / big value / optional body."""
    body_html = f"<div style='color:#6F6A5F; margin-top:0.4rem; font-size:0.92rem;'>{body}</div>" if body else ""
    st.markdown(
        f"""
        <div class="mp-card">
            <div class="label">{label}</div>
            <h3>{title}</h3>
            <div class="value">{value}</div>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(text: str, kind: str = "info"):
    """Render a coloured side-bar style callout. kind ∈ {info, warn, default}."""
    cls = f"callout {kind}".strip()
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


def stage_chip(stage: int) -> str:
    """Return HTML for a Stage 1 / 2 / 3 pill."""
    label = {1: "Stage 1 · Performing", 2: "Stage 2 · SICR", 3: "Stage 3 · NPA"}[stage]
    return f"<span class='stage-chip stage-{stage}'>{label}</span>"


def footer():
    """Render the consistent footer with circular reference."""
    st.markdown(
        """
        <div class="mp-footer">
            The Mountain Path Academy &nbsp;·&nbsp; Source: RBI Circular DOR.STR.REC.No.6/21.06.011/2026-27 dated 27-Apr-2026
            &nbsp;·&nbsp; Effective 1-Apr-2027
            <br/>Educational illustration only — not investment, accounting or regulatory advice.
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_setup(page_title: str, icon: str = "🏔️"):
    """Shorthand: set page config + apply theme. Call first in every page."""
    st.set_page_config(
        page_title=f"{page_title} · RBI ECL Directions, 2026",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_theme()


def fmt_inr(value: float, decimals: int = 0) -> str:
    """Format a number as Indian-style INR with lakh / crore awareness."""
    if value is None:
        return "—"
    sign = "-" if value < 0 else ""
    v = abs(float(value))
    if v >= 1e7:
        return f"{sign}₹{v/1e7:,.{max(decimals,2)}f} cr"
    if v >= 1e5:
        return f"{sign}₹{v/1e5:,.{max(decimals,2)}f} lakh"
    return f"{sign}₹{v:,.{decimals}f}"


def fmt_pct(value: float, decimals: int = 2) -> str:
    if value is None:
        return "—"
    return f"{value*100:,.{decimals}f}%"


# ---------------------------------------------------------------------------
# Table rendering helper — robust whether or not jinja2 is installed.
# pandas.DataFrame.style depends on jinja2; if it's missing we fall back to
# pre-formatted strings so the page still renders.
# ---------------------------------------------------------------------------

def _has_jinja2() -> bool:
    try:
        import jinja2  # noqa: F401
        return True
    except Exception:
        return False


def show_table(df, fmt: dict | None = None, **kwargs):
    """Render a DataFrame with optional column-format dict, jinja2-safe.

    Examples
    --------
    >>> show_table(df, {"Period ECL (₹)": "{:,.0f}", "PD": "{:.4f}"})
    """
    import pandas as _pd
    import streamlit as _st

    fmt = fmt or {}
    kwargs.setdefault("use_container_width", True)
    kwargs.setdefault("hide_index", True)

    if not fmt:
        _st.dataframe(df, **kwargs)
        return

    def _safe_apply(value, spec):
        """Apply a format spec, leaving the raw value if the spec doesn't fit."""
        if value is None or (isinstance(value, float) and _pd.isna(value)):
            return "—"
        try:
            return spec.format(value)
        except (ValueError, TypeError):
            return str(value)

    if _has_jinja2():
        try:
            # Wrap each formatter so jinja2/pandas don't crash on mixed-type cells
            safe_fmt = {col: (lambda v, _s=spec: _safe_apply(v, _s))
                        for col, spec in fmt.items() if col in df.columns}
            _st.dataframe(df.style.format(safe_fmt), **kwargs)
            return
        except Exception:
            pass  # fall through to manual formatting

    # Fallback: format columns to strings and display the raw DataFrame
    df2 = df.copy()
    for col, spec in fmt.items():
        if col in df2.columns:
            df2[col] = df2[col].apply(lambda x, _s=spec: _safe_apply(x, _s))
    _st.dataframe(df2, **kwargs)
