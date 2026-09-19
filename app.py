"""
Mental Health in Tech Survey — Interactive Streamlit Dashboard
Author: Shyam Jagani

Explore the 2014 OSMI Mental Health in Tech Survey (1,259 responses) and see
which demographic and workplace factors are associated with employees seeking
treatment for a mental health condition. Companion to the EDA notebook
Mental_Health_Tech_Survey_EDA.ipynb.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import load_data, encode_for_correlation, EMPLOYEE_ORDER, INTERFERE_ORDER, LEAVE_ORDER, AGE_LABELS

# ---------------------------------------------------------------- Palette
# Fixed categorical hue order (never cycled) — validated colorblind-safe set.
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLUE_SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DIVERGING = [[0, "#e34948"], [0.5, "#f0efec"], [1, "#2a78d6"]]
YES_NO_COLORS = {"Yes": CAT[0], "No": CAT[1]}
GENDER_COLORS = {"Male": CAT[0], "Female": CAT[4], "Other": CAT[2]}

st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=60, l=10, r=10, b=10),
)


def style(fig, title=None, height=420):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    if title:
        fig.update_layout(title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(137,135,129,0.25)")
    return fig


# ---------------------------------------------------------------- Data
df = load_data()

st.sidebar.title("🧠 Filters")
st.sidebar.caption("Filters apply to every section below.")

gender_sel = st.sidebar.multiselect("Gender", options=["Male", "Female", "Other"], default=["Male", "Female", "Other"])
age_sel = st.sidebar.slider("Age range", int(df["Age"].min()), int(df["Age"].max()), (18, 65))
country_options = sorted(df["country_grouped"].unique().tolist())
country_sel = st.sidebar.multiselect("Country (top 10 + Other)", options=country_options, default=country_options)
company_sel = st.sidebar.multiselect("Company size", options=EMPLOYEE_ORDER, default=EMPLOYEE_ORDER)

filtered = df[
    df["Gender"].isin(gender_sel)
    & df["Age"].between(age_sel[0], age_sel[1])
    & df["country_grouped"].isin(country_sel)
    & df["no_employees"].isin(company_sel)
].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Responses matching filters", f"{len(filtered):,} / {len(df):,}")
st.sidebar.caption(
    "Data: 2014 OSMI Mental Health in Tech Survey. "
    "Built for a data analytics internship project — see README for methodology."
)

section = st.sidebar.radio(
    "Section",
    ["Overview", "Demographics", "Workplace Factors", "Treatment Analysis", "Correlation Explorer", "Explore the Data"],
)

if filtered.empty:
    st.warning("No responses match the current filters. Try widening the filter selection in the sidebar.")
    st.stop()

# ================================================================== OVERVIEW
if section == "Overview":
    st.title("🧠 Mental Health in Tech Survey")
    st.markdown(
        "Interactive exploration of the **2014 OSMI Mental Health in Tech Survey** — "
        "1,259 responses on attitudes toward, and experiences of, mental health in the tech workplace. "
        "Use the sidebar to filter by gender, age, country, and company size."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Respondents", f"{len(filtered):,}")
    treated_pct = (filtered["treatment"] == "Yes").mean() * 100
    c2.metric("Sought treatment", f"{treated_pct:.1f}%")
    fh_pct = (filtered["family_history"] == "Yes").mean() * 100
    c3.metric("Family history of illness", f"{fh_pct:.1f}%")
    remote_pct = (filtered["remote_work"] == "Yes").mean() * 100
    c4.metric("Work remotely ≥50%", f"{remote_pct:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        counts = filtered["treatment"].value_counts().reindex(["Yes", "No"])
        fig = px.pie(
            values=counts.values, names=counts.index, hole=0.45,
            color=counts.index, color_discrete_map=YES_NO_COLORS,
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(style(fig, "Have Respondents Sought Treatment?", 360), use_container_width=True)
    with col2:
        counts = filtered["country_grouped"].value_counts()
        fig = px.bar(
            x=counts.values, y=counts.index, orientation="h",
            color_discrete_sequence=[CAT[0]],
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_xaxes(title="Respondents")
        fig.update_yaxes(title="")
        st.plotly_chart(style(fig, "Respondents by Country", 360), use_container_width=True)

    st.markdown(
        "**Key takeaway:** family history of mental illness and self-reported work interference are the "
        "strongest signals associated with treatment-seeking (see *Treatment Analysis* and *Correlation Explorer*), "
        "while awareness of employer benefits and care options — not just their existence — tracks closely with "
        "who actually gets help. Full methodology and business recommendations are in the companion EDA notebook and README."
    )

# ================================================================== DEMOGRAPHICS
elif section == "Demographics":
    st.title("Demographics")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(filtered, x="Age", nbins=30, color_discrete_sequence=[CAT[0]])
        st.plotly_chart(style(fig, "Age Distribution"), use_container_width=True)
    with col2:
        counts = filtered["Gender"].value_counts()
        fig = px.bar(
            x=counts.index, y=counts.values, color=counts.index,
            color_discrete_map=GENDER_COLORS, text=counts.values,
        )
        fig.update_traces(textposition="outside")
        fig.update_xaxes(title="Gender")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Gender Distribution (Standardized)"), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        counts = filtered["age_group"].value_counts().reindex(AGE_LABELS)
        fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[CAT[2]])
        fig.update_xaxes(title="Age Group")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Respondents by Age Group"), use_container_width=True)
    with col4:
        cross = pd.crosstab(filtered["age_group"], filtered["Gender"])[["Male", "Female", "Other"]].reindex(AGE_LABELS)
        fig = go.Figure()
        for gender in ["Male", "Female", "Other"]:
            fig.add_bar(name=gender, x=cross.index, y=cross[gender], marker_color=GENDER_COLORS[gender])
        fig.update_layout(barmode="stack")
        fig.update_xaxes(title="Age Group")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Age Group by Gender"), use_container_width=True)

    st.caption(
        "Gender was standardized from 49 raw free-text values into Male / Female / Other for meaningful comparison. "
        "The dataset skews male (~79%) and U.S./U.K.-based — see README for the full data-cleaning writeup."
    )

# ================================================================== WORKPLACE FACTORS
elif section == "Workplace Factors":
    st.title("Workplace Factors")

    col1, col2 = st.columns(2)
    with col1:
        counts = filtered["no_employees"].value_counts().reindex(EMPLOYEE_ORDER)
        fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[CAT[0]])
        fig.update_xaxes(title="Company Size")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Company Size Distribution"), use_container_width=True)
    with col2:
        counts = filtered["remote_work"].value_counts().reindex(["Yes", "No"])
        fig = px.pie(values=counts.values, names=counts.index, hole=0.45, color=counts.index, color_discrete_map=YES_NO_COLORS)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(style(fig, "Works Remotely ≥50% of the Time", 380), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        counts = filtered["benefits"].value_counts()
        fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[CAT[3]])
        fig.update_xaxes(title="Employer Provides Benefits")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Mental Health Benefits Availability"), use_container_width=True)
    with col4:
        counts = filtered["care_options"].value_counts()
        fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[CAT[6]])
        fig.update_xaxes(title="Aware of Care Options")
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, "Awareness of Care Options"), use_container_width=True)

    counts = filtered["leave"].value_counts().reindex(LEAVE_ORDER)
    fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[CAT[5]])
    fig.update_xaxes(title="Ease of Taking Medical Leave")
    fig.update_yaxes(title="Count")
    st.plotly_chart(style(fig, "Ease of Taking Medical Leave for a Mental Health Condition"), use_container_width=True)

    st.caption(
        "A third of respondents don't know whether benefits exist, and a similar share don't know what care "
        "options are available — communication, not just policy, is a recurring gap (see README recommendations)."
    )

# ================================================================== TREATMENT ANALYSIS
elif section == "Treatment Analysis":
    st.title("Treatment Analysis")
    st.markdown("How does treatment-seeking (`treatment`) vary across demographic and workplace factors?")

    factor = st.selectbox(
        "Compare treatment-seeking against:",
        options=["family_history", "Gender", "work_interfere", "no_employees", "benefits", "care_options", "leave", "remote_work"],
        format_func=lambda x: {
            "family_history": "Family History of Mental Illness",
            "Gender": "Gender",
            "work_interfere": "Work Interference Level",
            "no_employees": "Company Size",
            "benefits": "Mental Health Benefits",
            "care_options": "Care Options Awareness",
            "leave": "Ease of Taking Leave",
            "remote_work": "Remote Work",
        }[x],
    )

    order_map = {
        "no_employees": EMPLOYEE_ORDER,
        "work_interfere": INTERFERE_ORDER,
        "leave": LEAVE_ORDER,
        "Gender": ["Male", "Female", "Other"],
    }
    cat_order = order_map.get(factor, sorted(filtered[factor].dropna().unique().tolist()))

    col1, col2 = st.columns([3, 2])
    with col1:
        cross = pd.crosstab(filtered[factor], filtered["treatment"]).reindex(cat_order)
        fig = go.Figure()
        for outcome in ["Yes", "No"]:
            if outcome in cross.columns:
                fig.add_bar(name=f"Treatment: {outcome}", x=cross.index.astype(str), y=cross[outcome], marker_color=YES_NO_COLORS[outcome])
        fig.update_layout(barmode="group")
        fig.update_xaxes(title=factor)
        fig.update_yaxes(title="Count")
        st.plotly_chart(style(fig, f"Treatment-Seeking by {factor}", 440), use_container_width=True)
    with col2:
        rate = (pd.crosstab(filtered[factor], filtered["treatment"], normalize="index")["Yes"] * 100).reindex(cat_order)
        fig = px.bar(x=rate.index.astype(str), y=rate.values, color_discrete_sequence=[CAT[0]], text=[f"{v:.0f}%" for v in rate.values])
        fig.update_traces(textposition="outside")
        fig.update_xaxes(title=factor)
        fig.update_yaxes(title="% who sought treatment", range=[0, 100])
        st.plotly_chart(style(fig, "Treatment Rate (%)", 440), use_container_width=True)

    st.caption(
        "Family history and work-interference severity show the strongest relationship with treatment-seeking; "
        "company size shows the weakest. Full interpretation of each factor is in the EDA notebook (Charts 11–18)."
    )

# ================================================================== CORRELATION EXPLORER
elif section == "Correlation Explorer":
    st.title("Correlation Explorer")
    st.markdown("Encoded numeric view of how demographic and workplace variables relate to one another and to `treatment`.")

    enc = encode_for_correlation(filtered)
    corr = enc.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=DIVERGING, zmid=0, zmin=-1, zmax=1,
            text=corr.round(2).values, texttemplate="%{text}",
            colorbar=dict(title="corr"),
        )
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=560, title="Correlation Heatmap of Encoded Features")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("What correlates most with seeking treatment?")
    treatment_corr = corr["treatment"].drop("treatment").sort_values()
    fig2 = px.bar(
        x=treatment_corr.values, y=treatment_corr.index, orientation="h",
        color=treatment_corr.values, color_continuous_scale=DIVERGING, range_color=[-0.5, 0.5],
    )
    fig2.update_xaxes(title="Correlation with treatment")
    fig2.update_yaxes(title="")
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style(fig2, "Correlation with Treatment-Seeking", 420), use_container_width=True)

    st.caption(
        "`work_interfere` and `family_history` are the strongest correlates of treatment-seeking; `Age` and "
        "`remote_work` show almost none — matching the notebook's Chart 19–20 findings."
    )

# ================================================================== EXPLORE THE DATA
elif section == "Explore the Data":
    st.title("Explore the Data")
    st.markdown(f"Showing **{len(filtered):,}** of **{len(df):,}** total responses after sidebar filters.")
    st.dataframe(filtered.drop(columns=["age_group", "country_grouped"]), use_container_width=True, height=520)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_survey_data.csv", "text/csv")

    with st.expander("Column reference"):
        st.markdown(
            "See the README or the EDA notebook's *Understanding Your Variables* section for a full "
            "description of each survey column."
        )
