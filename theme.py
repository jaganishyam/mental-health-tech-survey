# theme + small html helpers for the dashboard. built entirely around
# green - the internationally recognized mental health awareness color -
# rather than pairing it with an unrelated brand color. everything from
# the page background to the buttons is a shade of green; the one
# exception is a small gold accent (the color used in a lot of awareness
# graphics alongside the ribbon) kept to a couple of decorative touches
# so it stays a supporting color, not a second theme.
#
# the actual data-series colors (CAT below) are a colorblind-checked set
# from the dataviz palette reference, re-validated for this light green
# surface - I kept those separate from the "chrome" colors (headers,
# buttons, cards) so the charts themselves stay accessible regardless of
# branding changes.

import plotly.graph_objects as go
import streamlit as st

BG = "#f2faf5"
CARD_BG = "#ffffff"
CARD_BORDER = "rgba(21,101,52,0.12)"
CARD_BORDER_HOVER = "rgba(21,128,61,0.4)"

TEXT_PRIMARY = "#0f3d24"
TEXT_SECONDARY = "#3f6b52"
TEXT_MUTED = "#7fa08d"

ACCENT_GREEN = "#16a34a"        # main brand accent
ACCENT_GREEN_DARK = "#14532d"   # ribbon-dark green, used for buttons/headings
ACCENT_GREEN_MID = "#22c55e"    # brighter mid-tone for gradients
ACCENT_GOLD = "#eab308"         # secondary accent, used sparingly

# validated against a light green surface with the dataviz skill's
# palette checker (all adjacent-pair CVD/contrast checks pass)
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
YES_NO = {"Yes": CAT[0], "No": CAT[1]}
GENDER_COLORS = {"Male": CAT[0], "Female": CAT[4], "Other": CAT[2]}
DIVERGING = [[0, CAT[7]], [0.5, "#f0efec"], [1, CAT[0]]]
SEQUENTIAL_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#256abf", "#184f95", "#0d366b"]


def base_layout(height=420, title=None):
    layout = dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, -apple-system, 'Segoe UI', sans-serif", color=TEXT_SECONDARY, size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=TEXT_SECONDARY)),
        margin=dict(t=56, l=10, r=10, b=10),
        height=height,
        hoverlabel=dict(bgcolor=CARD_BG, font_color=TEXT_PRIMARY, bordercolor=CARD_BORDER_HOVER),
    )
    if title:
        layout["title"] = dict(text=title, font=dict(color=TEXT_PRIMARY, size=15))
    return layout


def style(fig, title=None, height=420, showgrid_y=True):
    fig.update_layout(**base_layout(height=height, title=title))
    fig.update_xaxes(showgrid=False, color=TEXT_MUTED, linecolor="rgba(21,101,52,0.15)")
    fig.update_yaxes(showgrid=showgrid_y, gridcolor="rgba(21,101,52,0.1)", color=TEXT_MUTED, linecolor="rgba(21,101,52,0.15)")
    return fig


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}

        .stApp {{
            background: radial-gradient(ellipse 140% 90% at 15% -10%, #d9f2e1 0%, #eafbf1 35%, {BG} 70%), {BG};
            color: {TEXT_PRIMARY};
        }}

        section[data-testid="stSidebar"] {{ background: #e9f7ee; border-right: 1px solid {CARD_BORDER}; }}
        section[data-testid="stSidebar"] * {{ color: {TEXT_SECONDARY}; }}
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
            color: {TEXT_PRIMARY};
        }}

        h1, h2, h3, h4 {{ color: {TEXT_PRIMARY}; font-weight: 700; }}
        p, li, span {{ color: {TEXT_SECONDARY}; }}

        code {{
            background: rgba(22, 163, 74, 0.12) !important;
            color: {ACCENT_GREEN_DARK} !important;
            border-radius: 5px;
            padding: 1px 6px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85em;
            border: 1px solid rgba(22, 163, 74, 0.25);
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(120deg, #dff4e6, #eafaf1, #cdedd9, #e3f6ea, #dff4e6);
            background-size: 300% 300%;
            border: 1px solid rgba(21,128,61,0.25);
            border-radius: 18px;
            padding: 34px 40px;
            margin-bottom: 22px;
            animation: fadeInUp 0.6s ease both, heroGradientShift 14s ease-in-out infinite;
            box-shadow: 0 10px 30px -18px rgba(21,128,61,0.4);
        }}
        @keyframes heroGradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .hero {{ animation: none; }}
        }}
        .hero::after {{
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(234,179,8,0.16) 0%, rgba(234,179,8,0) 70%);
            pointer-events: none;
        }}
        .badge-pill {{
            display: inline-block;
            border: 1px solid rgba(21,128,61,0.4);
            color: {ACCENT_GREEN_DARK};
            background: rgba(22,163,74,0.1);
            border-radius: 999px;
            padding: 5px 16px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 18px;
            position: relative;
        }}
        .hero-title {{
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 0 14px 0;
            position: relative;
            background: linear-gradient(90deg, {ACCENT_GREEN_DARK} 0%, {ACCENT_GREEN} 55%, {ACCENT_GREEN_MID} 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-sub {{ font-size: 1.02rem; color: {TEXT_SECONDARY}; max-width: 900px; line-height: 1.6; position: relative; }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 6px 0 28px 0; }}
        @media (max-width: 900px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .kpi-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 20px 20px 16px 20px;
            box-shadow: 0 1px 3px rgba(21,101,52,0.06);
            animation: fadeInUp 0.6s ease both;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: {CARD_BORDER_HOVER};
            box-shadow: 0 10px 28px -16px rgba(21,128,61,0.4);
        }}
        .kpi-label {{ font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {TEXT_MUTED}; margin-bottom: 10px; }}
        .kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {TEXT_PRIMARY}; line-height: 1.1; }}
        .kpi-sub {{ font-size: 0.8rem; color: {ACCENT_GREEN_DARK}; margin-top: 6px; }}

        .content-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 18px;
            box-shadow: 0 1px 3px rgba(21,101,52,0.06);
            animation: fadeInUp 0.5s ease both;
        }}
        .section-title {{ font-size: 1.35rem; font-weight: 700; color: {TEXT_PRIMARY}; margin-bottom: 6px; }}
        .finding-item {{ margin-bottom: 10px; line-height: 1.55; }}
        .finding-item b {{ color: {TEXT_PRIMARY}; }}

        .tag {{
            display: inline-block;
            background: rgba(22,163,74,0.1);
            color: {ACCENT_GREEN_DARK};
            border: 1px solid rgba(22,163,74,0.3);
            border-radius: 999px;
            padding: 3px 12px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-right: 6px;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        div[data-testid="stMetricValue"] {{ color: {TEXT_PRIMARY}; }}

        /* nav bar buttons on the main page. targeting button[kind=...]
        directly rather than scoping through the column wrapper - streamlit
        has renamed that wrapper's testid before (column -> stColumn) and
        a scoped selector silently matches nothing when that happens, which
        is exactly what let the plain "p, li, span" rule above win out over
        the button's own text color. also resets the browser's default blue
        focus ring, which otherwise sits on whichever tab was clicked last. */
        button[kind="primary"] {{
            background: linear-gradient(90deg, {ACCENT_GREEN_DARK}, {ACCENT_GREEN}) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }}
        button[kind="primary"] p,
        button[kind="primary"] span,
        button[kind="primary"] div {{
            color: #ffffff !important;
        }}
        button[kind="secondary"] {{
            background: {CARD_BG} !important;
            border: 1px solid {CARD_BORDER} !important;
            color: {TEXT_SECONDARY} !important;
        }}
        button[kind="secondary"] p,
        button[kind="secondary"] span,
        button[kind="secondary"] div {{
            color: {TEXT_SECONDARY} !important;
        }}
        button[kind="secondary"]:hover {{
            border-color: rgba(22,163,74,0.45) !important;
            color: {ACCENT_GREEN_DARK} !important;
        }}
        button[kind="secondary"]:hover p,
        button[kind="secondary"]:hover span,
        button[kind="secondary"]:hover div {{
            color: {ACCENT_GREEN_DARK} !important;
        }}
        button[kind="primary"]:focus,
        button[kind="primary"]:focus-visible,
        button[kind="primary"]:active,
        button[kind="secondary"]:focus,
        button[kind="secondary"]:focus-visible,
        button[kind="secondary"]:active {{
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(22,163,74,0.3) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(badge, title, subtitle):
    st.markdown(
        f'<div class="hero"><span class="badge-pill">{badge}</span>'
        f'<div class="hero-title">{title}</div><div class="hero-sub">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def kpi_grid(items):
    # each card has to be a single-line string - if you split these across
    # multiple indented lines, markdown reads the gap between them as a
    # blank line and starts rendering the rest as a plain code block instead
    # of html (found this the hard way)
    cards = "".join(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'
        for label, value, sub in items
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)


def content_card_open(title=None):
    html = '<div class="content-card">'
    if title:
        html += f'<div class="section-title">{title}</div>'
    st.markdown(html, unsafe_allow_html=True)


def content_card_close():
    st.markdown("</div>", unsafe_allow_html=True)
