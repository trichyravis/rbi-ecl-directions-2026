"""Shared visual identity for the Mountain Path Academy — RBI ECL Directions app.

Design system ported from the Probability & Distributions app:
  Dark-blue / Gold palette, Playfair Display + Source Serif Pro typography,
  dark sidebar, brand banner, definition/example/Excel boxes, stat chips.
"""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Colour tokens — Mountain Path dark-blue / gold palette
# ---------------------------------------------------------------------------
DARKBLUE  = "#003366"
LIGHTBLUE = "#ADD8E6"
GOLD      = "#FFD700"
ACCENTRED = "#B22234"
EXCEL_GRN = "#217346"
PY_DARK   = "#1E3250"
OFFWHITE  = "#F7FAFC"

# Backward-compatible COLORS dict used by page files
COLORS = {
    "pine":      DARKBLUE,
    "moss":      "#004d99",
    "sage":      LIGHTBLUE,
    "parchment": OFFWHITE,
    "paper":     "#EBF0F5",
    "slate":     "#1a1a2e",
    "stone":     "#6F6A5F",
    "ember":     ACCENTRED,
    "gold":      GOLD,
    "snow":      "#FFFFFF",
}

STAGE_COLORS = {
    1: LIGHTBLUE,
    2: GOLD,
    3: ACCENTRED,
}

PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Source Serif Pro, Georgia, serif", "color": DARKBLUE, "size": 13},
        "paper_bgcolor": "#ffffff",
        "plot_bgcolor": "#ffffff",
        "colorway": [DARKBLUE, "#004d99", GOLD, ACCENTRED, LIGHTBLUE, "#6F6A5F"],
        "xaxis": {"gridcolor": "#e6eaf0", "zerolinecolor": "#e6eaf0", "linecolor": DARKBLUE},
        "yaxis": {"gridcolor": "#e6eaf0", "zerolinecolor": "#e6eaf0", "linecolor": DARKBLUE},
        "legend": {"bgcolor": "#ffffff", "bordercolor": DARKBLUE, "borderwidth": 1},
        "title": {"font": {"family": "Playfair Display, Georgia, serif", "size": 18, "color": DARKBLUE}},
        "margin": {"l": 60, "r": 20, "t": 60, "b": 50},
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+Pro:wght@400;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Serif Pro', Georgia, 'Times New Roman', serif;
}}

/* Container */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}}

/* Sidebar — dark blue */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARKBLUE} 0%, #001f3d 100%);
}}
[data-testid="stSidebar"] * {{
    color: #ffffff !important;
}}
[data-testid="stSidebar"] .stRadio > label > div {{
    color: #ffffff !important;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {GOLD} !important;
    font-family: 'Playfair Display', serif;
}}

/* Headings */
h1, h2, h3, h4 {{
    font-family: 'Playfair Display', Georgia, serif;
    color: {DARKBLUE};
    letter-spacing: -0.01em;
}}
h1 {{ font-weight: 900; }}
h2 {{ border-bottom: 3px solid {GOLD}; padding-bottom: 0.35rem; margin-top: 1.2rem; }}

/* Brand banner (replaces hero) */
.mp-brand-banner {{
    background: linear-gradient(135deg, {DARKBLUE} 0%, #001f3d 100%);
    color: #ffffff;
    padding: 22px 30px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    border-bottom: 4px solid {GOLD};
}}
.mp-brand-banner h1 {{
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    margin: 0;
    font-size: 2.2rem;
    letter-spacing: 2px;
    color: #ffffff;
}}
.mp-brand-banner .sub {{
    font-style: italic;
    color: {LIGHTBLUE};
    font-size: 1.05rem;
}}
.mp-brand-banner .dot {{
    color: {GOLD};
    font-weight: bold;
}}

/* hero — kept as alias to brand-banner for compatibility */
.hero {{
    background: linear-gradient(135deg, {DARKBLUE} 0%, #001f3d 100%);
    color: #ffffff;
    padding: 22px 30px;
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    border-bottom: 4px solid {GOLD};
}}
.hero h1 {{
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    color: #ffffff;
    margin: 0 0 0.4rem 0;
    font-size: 2.0rem;
    letter-spacing: 2px;
}}
.hero .eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.72rem;
    color: {GOLD};
    margin-bottom: 0.6rem;
}}
.hero p {{
    color: {LIGHTBLUE};
    margin: 0;
    font-size: 1.02rem;
    max-width: 80ch;
    font-style: italic;
}}

/* Page title / section */
.mp-title {{
    font-family: 'Playfair Display', serif;
    color: {DARKBLUE};
    font-size: 2.0rem;
    font-weight: 900;
    margin: 18px 0 4px 0;
    padding-bottom: 8px;
    border-bottom: 3px solid {GOLD};
}}
.mp-section {{
    font-family: 'Playfair Display', serif;
    color: {DARKBLUE};
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
    padding-left: 10px;
    border-left: 5px solid {GOLD};
}}

/* card — dark blue metric card */
.mp-card {{
    background: #ffffff;
    border: 1.5px solid {DARKBLUE}33;
    border-radius: 8px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}}
.mp-card .label {{
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: {GOLD};
    font-size: 0.72rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}}
.mp-card h3 {{
    margin: 0 0 0.4rem 0;
    color: {DARKBLUE};
    font-size: 1.05rem;
}}
.mp-card .value {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.6rem;
    color: {DARKBLUE};
    font-weight: 700;
}}

/* Stat chip row */
.stat-chip {{
    background: {DARKBLUE};
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 6px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}}
.stat-chip .label {{
    color: {GOLD};
    font-size: 0.82rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.stat-chip .val {{
    font-size: 1.35rem;
    font-weight: 700;
}}

/* Definition box (blue) */
.defn-box {{
    background: {LIGHTBLUE}33;
    border: 1.5px solid {DARKBLUE};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
}}
.defn-box .head {{
    background: {DARKBLUE};
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Example / illustration box (gold) */
.ex-box {{
    background: #fffbe6;
    border: 1.5px solid {GOLD};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
}}
.ex-box .head {{
    background: {GOLD};
    color: {DARKBLUE};
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Excel box (green) */
.xl-box {{
    background: #eaf7ef;
    border: 1.5px solid {EXCEL_GRN};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0 14px 0;
    font-family: 'Courier New', monospace;
    font-size: 0.95rem;
}}
.xl-box .head {{
    background: {EXCEL_GRN};
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-family: 'Source Serif Pro', serif;
    font-size: 0.95rem;
    letter-spacing: 1px;
}}

/* Summary box (gold tint) */
.sum-box {{
    background: #fff7d1;
    border: 1.5px solid {DARKBLUE};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 12px 0;
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
.stage-1 {{ background: {LIGHTBLUE}55; color: {DARKBLUE}; }}
.stage-2 {{ background: #FFF3C4; color: #8B6A1E; }}
.stage-3 {{ background: #F4D6C5; color: #7B3416; }}

/* call-out boxes — info/warn/default */
.callout {{
    border-left: 5px solid {GOLD};
    background: #fffbe6;
    padding: 0.9rem 1.1rem;
    border-radius: 6px;
    margin: 0.8rem 0;
    color: {DARKBLUE};
}}
.callout.warn  {{ border-left-color: {ACCENTRED}; background: #fde8e8; }}
.callout.info  {{ border-left-color: {DARKBLUE};  background: {LIGHTBLUE}33; }}
.callout strong {{ color: {DARKBLUE}; }}

/* Footer */
.mp-footer {{
    margin-top: 40px;
    padding: 14px;
    background: {DARKBLUE};
    color: #ffffff;
    text-align: center;
    border-top: 4px solid {GOLD};
    border-radius: 6px;
    font-size: 0.9rem;
}}
.mp-footer .gold {{ color: {GOLD}; font-weight: 700; }}

/* Metrics */
[data-testid="stMetric"] {{
    background: #ffffff;
    border: 1px solid {DARKBLUE}33;
    border-radius: 6px;
    padding: 8px 10px;
}}
[data-testid="stMetricLabel"] {{
    color: {DARKBLUE} !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Playfair Display', Georgia, serif;
    color: {DARKBLUE};
}}

/* Tables */
.dataframe th {{
    background: {DARKBLUE} !important;
    color: #ffffff !important;
}}
.stDataFrame, .stTable {{
    border-radius: 8px;
    overflow: hidden;
}}

/* Buttons */
.stButton>button {{
    background: {DARKBLUE};
    color: #ffffff;
    border: 1.5px solid {GOLD};
    border-radius: 6px;
    font-weight: 600;
}}
.stButton>button:hover {{
    background: {GOLD};
    color: {DARKBLUE};
    border: 1.5px solid {DARKBLUE};
}}

/* Tab polish */
.stTabs [data-baseweb="tab-list"] button {{
    font-family: 'Source Serif Pro', sans-serif;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    color: {DARKBLUE} !important;
    border-bottom-color: {GOLD} !important;
}}
</style>
"""


def apply_theme():
    """Inject the global CSS. Call at the top of every page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str, eyebrow: str = "RBI ECL Directions, 2026"):
    """A consistent dark-blue banner for each page."""
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


def brand_banner():
    """Full Mountain Path brand banner (used on Home page)."""
    st.markdown(
        f"""
        <div class="mp-brand-banner">
            <h1>THE MOUNTAIN PATH</h1>
            <div class="sub">World of Finance <span class="dot">&bull;</span> themountainpathacademy.com</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(text: str):
    """A gold-bordered section header."""
    st.markdown(f'<div class="mp-section">{text}</div>', unsafe_allow_html=True)


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


def defn_box(title: str, body_md: str):
    """Definition box — blue theme."""
    st.markdown(
        f'<div class="defn-box"><span class="head">{title}</span><br>{body_md}</div>',
        unsafe_allow_html=True,
    )


def ex_box(title: str, body_md: str):
    """Example / illustration box — gold theme."""
    st.markdown(
        f'<div class="ex-box"><span class="head">{title}</span><br>{body_md}</div>',
        unsafe_allow_html=True,
    )


def xl_box(title: str, body_md: str):
    """Excel formula box — green theme."""
    st.markdown(
        f'<div class="xl-box"><span class="head">{title}</span><br>{body_md}</div>',
        unsafe_allow_html=True,
    )


def sum_box(body_md: str):
    """Summary box — gold tint."""
    st.markdown(f'<div class="sum-box">{body_md}</div>', unsafe_allow_html=True)


def stat_chip_row(items):
    """Row of dark-blue stat chips. items = list of (label, value) tuples."""
    cols = st.columns(len(items))
    for c, (lbl, val) in zip(cols, items):
        with c:
            st.markdown(
                f'<div class="stat-chip"><div class="label">{lbl}</div>'
                f'<div class="val">{val}</div></div>',
                unsafe_allow_html=True,
            )


def callout(text: str, kind: str = "info"):
    """Render a coloured side-bar style callout. kind in {info, warn, default}."""
    cls = f"callout {kind}".strip()
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


def stage_chip(stage: int) -> str:
    """Return HTML for a Stage 1 / 2 / 3 pill."""
    label = {1: "Stage 1 - Performing", 2: "Stage 2 - SICR", 3: "Stage 3 - NPA"}[stage]
    return f"<span class='stage-chip stage-{stage}'>{label}</span>"


def footer():
    """Render the consistent dark-blue footer."""
    st.markdown(
        f"""
        <div class="mp-footer">
            <span class="gold">The Mountain Path &mdash; World of Finance</span> &nbsp;&bull;&nbsp;
            Prof. V. Ravichandran &nbsp;&bull;&nbsp;
            <i>Bridging Theory with Practice</i> &nbsp;&bull;&nbsp;
            <a href="https://themountainpathacademy.com" target="_blank" style="color:{GOLD};text-decoration:none;">themountainpathacademy.com</a>
            <br/>
            Source: RBI Circular DOR.STR.REC.No.6/21.06.011/2026-27 dated 27-Apr-2026
            &nbsp;&bull;&nbsp; Effective 1-Apr-2027
            <br/>Educational illustration only &mdash; not investment, accounting or regulatory advice.
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_setup(page_title: str, icon: str = "🏔️"):
    """Shorthand: set page config + apply theme. Call first in every page."""
    st.set_page_config(
        page_title=f"{page_title} - RBI ECL Directions, 2026",
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
# Table rendering helper
# ---------------------------------------------------------------------------

def _has_jinja2() -> bool:
    try:
        import jinja2  # noqa: F401
        return True
    except Exception:
        return False


def show_table(df, fmt: dict | None = None, **kwargs):
    """Render a DataFrame with optional column-format dict, jinja2-safe."""
    import pandas as _pd
    import streamlit as _st

    fmt = fmt or {}
    kwargs.setdefault("use_container_width", True)
    kwargs.setdefault("hide_index", True)

    if not fmt:
        _st.dataframe(df, **kwargs)
        return

    def _safe_apply(value, spec):
        if value is None or (isinstance(value, float) and _pd.isna(value)):
            return "—"
        try:
            return spec.format(value)
        except (ValueError, TypeError):
            return str(value)

    if _has_jinja2():
        try:
            safe_fmt = {col: (lambda v, _s=spec: _safe_apply(v, _s))
                        for col, spec in fmt.items() if col in df.columns}
            _st.dataframe(df.style.format(safe_fmt), **kwargs)
            return
        except Exception:
            pass

    df2 = df.copy()
    for col, spec in fmt.items():
        if col in df2.columns:
            df2[col] = df2[col].apply(lambda x, _s=spec: _safe_apply(x, _s))
    _st.dataframe(df2, **kwargs)
