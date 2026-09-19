# theme + small html helpers for the dashboard. colors are built around
# green, since that's the color generally tied to mental health awareness
# (the awareness ribbon is green) rather than an arbitrary brand palette.
#
# the actual data-series colors (CAT below) are a colorblind-checked set
# from the dataviz palette reference - I kept those as-is and only changed
# the "chrome" colors (headers, buttons, cards) to green, so the charts
# themselves stay accessible.

import plotly.graph_objects as go
import streamlit as st

BG = "#0a0e17"
CARD_BG = "#131826"
CARD_BORDER = "rgba(255,255,255,0.08)"
CARD_BORDER_HOVER = "rgba(34,197,94,0.35)"

TEXT_PRIMARY = "#f1f5f9"
TEXT_SECONDARY = "#9aa5b8"
TEXT_MUTED = "#657089"

ACCENT_GREEN = "#22c55e"       # main brand accent
ACCENT_GREEN_LIGHT = "#86efac"
ACCENT_TEAL = "#14b8a6"

# validated against this app's dark surface with the dataviz skill's
# palette checker (all adjacent-pair CVD/contrast checks pass)
CAT = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
YES_NO = {"Yes": CAT[0], "No": CAT[1]}
GENDER_COLORS = {"Male": CAT[0], "Female": CAT[4], "Other": CAT[2]}
DIVERGING = [[0, CAT[7]], [0.5, "#2c2c2a"], [1, CAT[0]]]
SEQUENTIAL_BLUE = ["#10141f", "#152238", "#1b3459", "#204a82", "#2a63ad", "#3987e5", "#7fb0ee", "#c4dcf9"]


def base_layout(height=420, title=None):
    layout = dict(
        template="plotly_dark",
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
    fig.update_xaxes(showgrid=False, color=TEXT_MUTED, linecolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(showgrid=showgrid_y, gridcolor="rgba(255,255,255,0.06)", color=TEXT_MUTED, linecolor="rgba(255,255,255,0.08)")
    return fig


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}

        .stApp {{
            background: radial-gradient(ellipse 120% 80% at 20% -10%, #10231a 0%, {BG} 45%), {BG};
            color: {TEXT_PRIMARY};
        }}

        section[data-testid="stSidebar"] {{ background: #070a10; border-right: 1px solid {CARD_BORDER}; }}
        section[data-testid="stSidebar"] * {{ color: {TEXT_SECONDARY}; }}
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
            color: {TEXT_PRIMARY};
        }}

        h1, h2, h3, h4 {{ color: {TEXT_PRIMARY}; font-weight: 700; }}
        p, li, span {{ color: {TEXT_SECONDARY}; }}

        code {{
            background: rgba(34, 197, 94, 0.12) !important;
            color: {ACCENT_GREEN_LIGHT} !important;
            border-radius: 5px;
            padding: 1px 6px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85em;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }}

        .hero {{
            background: linear-gradient(135deg, #0e2418 0%, #16233d 45%, #142c22 100%);
            border: 1px solid rgba(34,197,94,0.2);
            border-radius: 18px;
            padding: 34px 40px;
            margin-bottom: 22px;
            animation: fadeInUp 0.6s ease both;
            box-shadow: 0 0 60px -20px rgba(34,197,94,0.25);
        }}
        .badge-pill {{
            display: inline-block;
            border: 1px solid rgba(34,197,94,0.4);
            color: {ACCENT_GREEN_LIGHT};
            background: rgba(34,197,94,0.08);
            border-radius: 999px;
            padding: 5px 16px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 18px;
        }}
        .hero-title {{
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 0 14px 0;
            background: linear-gradient(90deg, {ACCENT_GREEN_LIGHT} 0%, {ACCENT_TEAL} 60%, {ACCENT_GREEN} 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-sub {{ font-size: 1.02rem; color: {TEXT_SECONDARY}; max-width: 900px; line-height: 1.6; }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 6px 0 28px 0; }}
        @media (max-width: 900px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .kpi-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 20px 20px 16px 20px;
            animation: fadeInUp 0.6s ease both;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: {CARD_BORDER_HOVER};
            box-shadow: 0 8px 30px -12px rgba(34,197,94,0.35);
        }}
        .kpi-label {{ font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {TEXT_MUTED}; margin-bottom: 10px; }}
        .kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {TEXT_PRIMARY}; line-height: 1.1; }}
        .kpi-sub {{ font-size: 0.8rem; color: {ACCENT_GREEN_LIGHT}; margin-top: 6px; }}

        .content-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 18px;
            animation: fadeInUp 0.5s ease both;
        }}
        .section-title {{ font-size: 1.35rem; font-weight: 700; color: {TEXT_PRIMARY}; margin-bottom: 6px; }}
        .finding-item {{ margin-bottom: 10px; line-height: 1.55; }}
        .finding-item b {{ color: {TEXT_PRIMARY}; }}

        .tag {{
            display: inline-block;
            background: rgba(20,184,166,0.12);
            color: {ACCENT_TEAL};
            border: 1px solid rgba(20,184,166,0.3);
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

        /* nav bar buttons on the main page */
        div[data-testid="column"] button[kind="primary"] {{
            background: linear-gradient(90deg, {ACCENT_GREEN_LIGHT}, {ACCENT_TEAL});
            border: none;
            color: #06120c;
            font-weight: 700;
        }}
        div[data-testid="column"] button[kind="secondary"] {{
            background: transparent;
            border: 1px solid {CARD_BORDER};
            color: {TEXT_SECONDARY};
        }}
        div[data-testid="column"] button[kind="secondary"]:hover {{
            border-color: rgba(34,197,94,0.4);
            color: {ACCENT_GREEN_LIGHT};
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
