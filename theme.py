"""
Dark, gradient-accented theme for the Mental Health in Tech Survey app —
custom CSS injection + small HTML component builders (hero, badge, KPI
cards) + the chart color palette used across all Plotly figures.

Categorical palette validated colorblind-safe against this app's dark
surface with the dataviz skill's validator (scripts/validate_palette.js):
all checks pass at --mode dark --surface "#10141f".
"""

import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------- Palette
BG = "#0a0e17"
SIDEBAR_BG = "#070a10"
SURFACE = "#10141f"
CARD_BG = "#131826"
CARD_BORDER = "rgba(255,255,255,0.08)"
CARD_BORDER_HOVER = "rgba(56,189,248,0.35)"

TEXT_PRIMARY = "#f1f5f9"
TEXT_SECONDARY = "#9aa5b8"
TEXT_MUTED = "#657089"

ACCENT_CYAN = "#38bdf8"
ACCENT_PURPLE = "#a78bfa"
ACCENT_TEAL = "#2dd4bf"

# Fixed categorical order — validated CVD-safe on this app's dark surface.
CAT = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
YES_NO = {"Yes": CAT[0], "No": CAT[1]}
GENDER_COLORS = {"Male": CAT[0], "Female": CAT[4], "Other": CAT[2]}
DIVERGING = [[0, CAT[7]], [0.5, "#2c2c2a"], [1, CAT[0]]]
SEQUENTIAL_BLUE = ["#10141f", "#152238", "#1b3459", "#204a82", "#2a63ad", "#3987e5", "#7fb0ee", "#c4dcf9"]

PLOTLY_TEMPLATE = "plotly_dark"


def base_layout(height=420, title=None):
    layout = dict(
        template=PLOTLY_TEMPLATE,
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
    fig.update_yaxes(
        showgrid=showgrid_y, gridcolor="rgba(255,255,255,0.06)", color=TEXT_MUTED, linecolor="rgba(255,255,255,0.08)"
    )
    return fig


# ---------------------------------------------------------------- CSS
def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}

        .stApp {{
            background: radial-gradient(ellipse 120% 80% at 20% -10%, #142033 0%, {BG} 45%), {BG};
            color: {TEXT_PRIMARY};
        }}

        section[data-testid="stSidebar"] {{
            background: {SIDEBAR_BG};
            border-right: 1px solid {CARD_BORDER};
        }}
        section[data-testid="stSidebar"] * {{ color: {TEXT_SECONDARY}; }}
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
            color: {TEXT_PRIMARY};
        }}

        /* Sidebar radio nav styled as a clean list */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
            padding: 7px 10px;
            border-radius: 8px;
            transition: background 0.15s ease, transform 0.15s ease;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
            background: rgba(56,189,248,0.08);
            transform: translateX(2px);
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label span:first-child div {{
            border-color: {ACCENT_CYAN} !important;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
            font-size: 0.94rem;
            font-weight: 500;
        }}

        h1, h2, h3, h4 {{ color: {TEXT_PRIMARY}; font-weight: 700; }}
        p, li, span {{ color: {TEXT_SECONDARY}; }}

        code {{
            background: rgba(45, 212, 191, 0.12) !important;
            color: {ACCENT_TEAL} !important;
            border-radius: 5px;
            padding: 1px 6px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85em;
            border: 1px solid rgba(45, 212, 191, 0.18);
        }}

        /* ---------------- Hero ---------------- */
        .hero {{
            background: linear-gradient(135deg, #0e2438 0%, #16233d 45%, #1c1a34 100%);
            border: 1px solid rgba(56,189,248,0.18);
            border-radius: 18px;
            padding: 34px 40px;
            margin-bottom: 22px;
            animation: fadeInUp 0.6s ease both;
            box-shadow: 0 0 60px -20px rgba(56,189,248,0.25);
        }}
        .badge-pill {{
            display: inline-block;
            border: 1px solid rgba(56,189,248,0.4);
            color: {ACCENT_CYAN};
            background: rgba(56,189,248,0.08);
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
            background: linear-gradient(90deg, #7dd3fc 0%, {ACCENT_CYAN} 35%, {ACCENT_PURPLE} 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-sub {{
            font-size: 1.02rem;
            color: {TEXT_SECONDARY};
            max-width: 900px;
            line-height: 1.6;
        }}

        /* ---------------- KPI cards ---------------- */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 6px 0 28px 0;
        }}
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
            box-shadow: 0 8px 30px -12px rgba(56,189,248,0.35);
        }}
        .kpi-label {{
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {TEXT_MUTED};
            margin-bottom: 10px;
        }}
        .kpi-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {TEXT_PRIMARY};
            line-height: 1.1;
        }}
        .kpi-sub {{
            font-size: 0.8rem;
            color: {ACCENT_CYAN};
            margin-top: 6px;
        }}

        /* ---------------- Generic content card ---------------- */
        .content-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 18px;
            animation: fadeInUp 0.5s ease both;
        }}
        .section-title {{
            font-size: 1.35rem;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            margin-bottom: 6px;
        }}
        .finding-item {{ margin-bottom: 10px; line-height: 1.55; }}
        .finding-item b {{ color: {TEXT_PRIMARY}; }}

        .tag {{
            display: inline-block;
            background: rgba(167,139,250,0.12);
            color: {ACCENT_PURPLE};
            border: 1px solid rgba(167,139,250,0.3);
            border-radius: 999px;
            padding: 3px 12px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-right: 6px;
        }}

        .disclaimer {{
            background: rgba(217,89,38,0.08);
            border: 1px solid rgba(217,89,38,0.3);
            border-radius: 12px;
            padding: 14px 18px;
            color: #f3b596;
            font-size: 0.88rem;
            line-height: 1.5;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Streamlit chrome cleanup */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        div[data-testid="stMetricValue"] {{ color: {TEXT_PRIMARY}; }}
        .stButton > button, div[data-testid="stFormSubmitButton"] > button {{
            background: linear-gradient(90deg, {ACCENT_CYAN}, {ACCENT_PURPLE});
            color: #06121f;
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: 10px 22px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px -8px rgba(56,189,248,0.5);
            color: #06121f;
        }}
        .stButton > button p, div[data-testid="stFormSubmitButton"] > button p {{
            color: #06121f;
            font-weight: 700;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- Components
def hero(badge, title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <span class="badge-pill">{badge}</span>
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_grid(items):
    """items: list of (label, value, sub) tuples.

    Built as single-line HTML fragments deliberately: a multi-line indented
    fragment joined with others can produce a whitespace-only line between
    cards, which Markdown treats as a blank line ending the raw-HTML block —
    everything after the first card then renders as literal text instead of
    styled HTML.
    """
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


def gauge(value, title, color=ACCENT_CYAN, max_value=100):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%", "font": {"color": TEXT_PRIMARY, "size": 40}},
            title={"text": title, "font": {"color": TEXT_SECONDARY, "size": 14}},
            gauge={
                "axis": {"range": [0, max_value], "tickcolor": TEXT_MUTED, "tickfont": {"color": TEXT_MUTED}},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, max_value * 0.33], "color": "rgba(255,255,255,0.04)"},
                    {"range": [max_value * 0.33, max_value * 0.66], "color": "rgba(255,255,255,0.07)"},
                    {"range": [max_value * 0.66, max_value], "color": "rgba(255,255,255,0.10)"},
                ],
            },
        )
    )
    fig.update_layout(**base_layout(height=280))
    return fig
