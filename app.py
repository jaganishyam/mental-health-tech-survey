"""
Mental Health in Tech Survey — Analytics & Prediction
A data-analytics portfolio dashboard on the 2014 OSMI Mental Health in Tech
Survey: detailed EDA with a mix of uncommon chart types, a trained
predictive model, and a live "try it yourself" prediction tool.

Author: Shyam Jagani
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import theme
from model import ALL_FEATURES, FORM_FEATURES, predict_probability, train_models
from utils import (
    AGE_LABELS,
    EMPLOYEE_ORDER,
    INTERFERE_ORDER,
    LEAVE_ORDER,
    encode_for_correlation,
    get_mode_row,
    load_data,
    workplace_support_index,
)

st.set_page_config(page_title="Mental Health in Tech Survey", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
theme.inject_css()

df = load_data()
mode_row = get_mode_row(df)
model_results, best_model_name = train_models(df)
best = model_results[best_model_name]

# ================================================================== SIDEBAR
st.sidebar.markdown(
    """
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">
        <span style="font-size:1.4rem;">🧠</span>
        <span style="font-size:1.05rem;font-weight:700;color:#f1f5f9;">Mental Health in Tech Survey</span>
    </div>
    <div style="color:#657089;font-size:0.82rem;margin-bottom:18px;">OSMI Survey · EDA + ML capstone</div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("**Navigate**")

NAV = [
    ("🏠", "Overview"),
    ("🔎", "Explore & Segment"),
    ("🧬", "Correlations & Drivers"),
    ("🤖", "Model Performance"),
    ("🔮", "Try the Prediction Tool"),
    ("📈", "Response Timeline"),
    ("📌", "Recommendations & About"),
]
labels = [f"{icon}  {name}" for icon, name in NAV]
choice = st.sidebar.radio("Navigate", labels, label_visibility="collapsed")
section = choice.split("  ", 1)[1]

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="color:#9aa5b8;font-size:0.82rem;line-height:1.6;">
    Dataset: 2014 OSMI Mental Health in Tech Survey ({len(df):,} respondents).
    Response timestamps span Aug 2014 – Feb 2016 (see <i>Response Timeline</i>).
    </div>
    <div style="margin-top:14px;color:#657089;font-size:0.8rem;">
    Built by <b style="color:#9aa5b8;">Shyam Jagani</b> — data analytics internship / portfolio project.
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================================================== OVERVIEW
if section == "Overview":
    theme.hero(
        "EDA + Predictive Analytics · Data Analyst Portfolio Project",
        "Mental Health in Tech Survey — Analytics &amp; Insights",
        "What drives an employee in tech to seek treatment for a mental health condition, and what should "
        "employers change to remove barriers to that treatment? This app turns 1,259 responses from the 2014 "
        "OSMI survey into an interactive dashboard, a validated ML model, and a live prediction tool.",
    )

    top_feature = "Family History of Mental Illness"
    rf_importance_preview = model_results["Random Forest"].feature_importance
    if rf_importance_preview is not None and len(rf_importance_preview) > 0:
        top_feature = rf_importance_preview.iloc[0]["feature"]

    theme.kpi_grid(
        [
            ("Respondents Analyzed", f"{len(df):,}", "2014 OSMI survey, 18 model features"),
            ("Sought Treatment", f"{(df['treatment'] == 'Yes').mean() * 100:.1f}%", "of respondents overall"),
            ("Best Model ROC-AUC", f"{best.roc_auc:.3f}", best_model_name),
            ("Top Predictor", top_feature, "highest feature importance"),
        ]
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        theme.content_card_open("Project story")
        st.markdown(
            f"""
The raw survey arrives with real-world scars: 49 inconsistent spellings of `Gender`, ages ranging from
-1,726 to 99,999,999,999, and null-heavy columns like `state` (40.9% missing) and `comments` (87% missing).
A deliberate cleaning pass — capping age to a realistic 15–100 range, collapsing gender into 3 consistent
buckets, and treating missing `work_interfere` as its own meaningful category — brings the data to zero
remaining unexplained nulls before any chart or model is trusted.

From there the analysis moves through three layers: **who** responded (demographics), **what workplace
policies** they experience (benefits, leave, anonymity, company size), and **whether** they sought
treatment for a mental health condition — the outcome variable tied together in the *Correlations &amp;
Drivers* and *Model Performance* sections. A Random Forest and a Logistic Regression model are trained on
18 cleaned features to quantify which factors matter most, and the *Try the Prediction Tool* page lets you
enter your own answers and see the model's output live.
            """
        )
        theme.content_card_close()
    with col2:
        theme.content_card_open("Key findings")
        st.markdown(
            """
<div class="finding-item">📌 <b>Family history</b> and <b>work interference</b> are, by a wide margin, the two strongest predictors of treatment-seeking — well ahead of country, gender, or company size.</div>
<div class="finding-item">📌 Structural workplace factors — <b>care options awareness</b>, <b>anonymity</b>, and <b>ease of leave</b> — correlate with treatment-seeking more than company size does.</div>
<div class="finding-item">📌 <b>Male respondents</b> (79% of the sample) seek treatment at a meaningfully lower rate than Female/Other respondents.</div>
<div class="finding-item">📌 A third of respondents don't know what mental health benefits or care options their employer even offers — a low-cost, high-leverage fix.</div>
<div class="finding-item">📌 <b>Age</b> and <b>remote work</b> show almost no relationship with treatment-seeking in this dataset.</div>
            """,
            unsafe_allow_html=True,
        )
        theme.content_card_close()

# ================================================================== EXPLORE & SEGMENT
elif section == "Explore & Segment":
    st.markdown("## 🔎 Explore &amp; Segment")
    st.caption("Filter the sample and explore demographic and workplace patterns with a mix of chart types.")

    fc1, fc2, fc3, fc4 = st.columns(4)
    gender_sel = fc1.multiselect("Gender", ["Male", "Female", "Other"], default=["Male", "Female", "Other"])
    age_sel = fc2.slider("Age range", int(df["Age"].min()), int(df["Age"].max()), (18, 65))
    country_sel = fc3.multiselect(
        "Country", sorted(df["country_grouped"].unique()), default=sorted(df["country_grouped"].unique())
    )
    company_sel = fc4.multiselect("Company size", EMPLOYEE_ORDER, default=EMPLOYEE_ORDER)

    fdf = df[
        df["Gender"].isin(gender_sel)
        & df["Age"].between(age_sel[0], age_sel[1])
        & df["country_grouped"].isin(country_sel)
        & df["no_employees"].isin(company_sel)
    ].copy()

    if fdf.empty:
        st.warning("No responses match these filters.")
        st.stop()

    m1, m2, m3 = st.columns(3)
    m1.metric("Respondents", f"{len(fdf):,}")
    m2.metric("Sought treatment", f"{(fdf['treatment'] == 'Yes').mean() * 100:.1f}%")
    m3.metric("Avg. age", f"{fdf['Age'].mean():.1f}")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.violin(
            fdf, x="treatment", y="Age", color="treatment", box=True, points=False,
            category_orders={"treatment": ["Yes", "No"]}, color_discrete_map=theme.YES_NO,
        )
        st.plotly_chart(theme.style(fig, "Age Distribution by Treatment-Seeking (Violin Plot)"), use_container_width=True)
    with c2:
        sun = fdf.groupby(["Gender", "family_history", "treatment"]).size().reset_index(name="count")
        fig = px.sunburst(
            sun, path=["Gender", "family_history", "treatment"], values="count",
            color_discrete_sequence=theme.CAT,
        )
        fig.update_traces(hovertemplate="%{label}<br>%{value} respondents<extra></extra>")
        st.plotly_chart(theme.style(fig, "Gender → Family History → Treatment (Sunburst)", height=440), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        tree = fdf.groupby(["country_grouped", "no_employees"], observed=True).size().reset_index(name="count")
        tree = tree[tree["count"] > 0]
        fig = px.treemap(
            tree, path=["country_grouped", "no_employees"], values="count", color="count",
            color_continuous_scale=theme.SEQUENTIAL_BLUE,
        )
        fig.update_traces(hovertemplate="%{label}<br>%{value} respondents<extra></extra>")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(theme.style(fig, "Country → Company Size (Treemap, sized by respondents)", height=440), use_container_width=True)
    with c4:
        bubble = (
            fdf.groupby("country_grouped")
            .agg(avg_age=("Age", "mean"), count=("Age", "size"), treatment_rate=("treatment", lambda s: (s == "Yes").mean() * 100))
            .reset_index()
        )
        fig = px.scatter(
            bubble, x="avg_age", y="treatment_rate", size="count", color="treatment_rate",
            text="country_grouped", size_max=55, color_continuous_scale=theme.SEQUENTIAL_BLUE,
        )
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="rgba(255,255,255,0.25)")))
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(title="Average Age")
        fig.update_yaxes(title="Treatment Rate (%)")
        st.plotly_chart(theme.style(fig, "Country Bubble Map: Age vs. Treatment Rate vs. Sample Size", height=440), use_container_width=True)

    counts = fdf["benefits"].value_counts()
    order = ["Yes", "No", "Don't know"]
    cross = pd.crosstab(fdf["benefits"], fdf["treatment"]).reindex(order)
    fig = go.Figure()
    for outcome in ["Yes", "No"]:
        if outcome in cross.columns:
            fig.add_bar(name=f"Treatment: {outcome}", x=cross.index, y=cross[outcome], marker_color=theme.YES_NO[outcome])
    fig.update_layout(barmode="group")
    fig.update_xaxes(title="Employer Provides Mental Health Benefits")
    fig.update_yaxes(title="Count")
    st.plotly_chart(theme.style(fig, "Treatment-Seeking by Benefits Availability", height=380), use_container_width=True)

# ================================================================== CORRELATIONS & DRIVERS
elif section == "Correlations & Drivers":
    st.markdown("## 🧬 Correlations &amp; Drivers")
    st.caption("How workplace and demographic factors relate to each other and flow into the treatment outcome.")

    enc = encode_for_correlation(df)
    corr = enc.corr()

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values, x=corr.columns, y=corr.columns, colorscale=theme.DIVERGING, zmid=0, zmin=-1, zmax=1,
                text=corr.round(2).values, texttemplate="%{text}",
                colorbar=dict(title="corr", tickfont=dict(color=theme.TEXT_MUTED)),
            )
        )
        fig.update_layout(**theme.base_layout(height=520, title="Correlation Heatmap of Encoded Features"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        treatment_corr = corr["treatment"].drop("treatment").sort_values()
        colors = [theme.CAT[2] if v >= 0 else theme.CAT[7] for v in treatment_corr.values]
        fig = go.Figure(go.Bar(x=treatment_corr.values, y=treatment_corr.index, orientation="h", marker_color=colors))
        fig.update_xaxes(title="Correlation with treatment")
        st.plotly_chart(theme.style(fig, "Correlation with Treatment-Seeking", height=520), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        support = workplace_support_index(df)
        factors = list(support["factor"].unique())
        fig = go.Figure()
        for outcome in ["Yes", "No"]:
            sub = support[support["treatment"] == outcome].set_index("factor").reindex(factors)
            fig.add_trace(
                go.Scatterpolar(
                    r=sub["score"], theta=factors, fill="toself", name=f"Sought treatment: {outcome}",
                    line_color=theme.YES_NO[outcome], opacity=0.75,
                )
            )
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0.02)",
                radialaxis=dict(visible=True, range=[0, 100], color=theme.TEXT_MUTED, gridcolor="rgba(255,255,255,0.08)"),
                angularaxis=dict(color=theme.TEXT_SECONDARY, gridcolor="rgba(255,255,255,0.08)"),
            ),
        )
        fig.update_layout(**theme.base_layout(height=460, title="Workplace Support Index by Treatment Status (Radar)"))
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        work_bucket = {
            "Never": "Never / Rarely", "Rarely": "Never / Rarely", "Not applicable": "N/A",
            "Sometimes": "Sometimes / Often", "Often": "Sometimes / Often",
        }
        sdf = df.copy()
        sdf["interfere_bucket"] = sdf["work_interfere"].astype(str).map(work_bucket)

        fh_nodes = ["Family History: Yes", "Family History: No"]
        wi_nodes = ["Never / Rarely", "Sometimes / Often", "N/A"]
        tr_nodes = ["Treatment: Yes", "Treatment: No"]
        all_nodes = fh_nodes + wi_nodes + tr_nodes
        idx = {n: i for i, n in enumerate(all_nodes)}

        src, tgt, val = [], [], []
        g1 = sdf.groupby(["family_history", "interfere_bucket"]).size().reset_index(name="n")
        for _, r in g1.iterrows():
            src.append(idx[f"Family History: {r['family_history']}"])
            tgt.append(idx[r["interfere_bucket"]])
            val.append(r["n"])
        g2 = sdf.groupby(["interfere_bucket", "treatment"]).size().reset_index(name="n")
        for _, r in g2.iterrows():
            src.append(idx[r["interfere_bucket"]])
            tgt.append(idx[f"Treatment: {r['treatment']}"])
            val.append(r["n"])

        node_colors = [theme.CAT[0], theme.CAT[1]] + [theme.CAT[2], theme.CAT[3], theme.CAT[5]] + [theme.CAT[0], theme.CAT[1]]
        fig = go.Figure(
            go.Sankey(
                node=dict(label=all_nodes, color=node_colors, pad=18, thickness=16, line=dict(color="rgba(0,0,0,0)")),
                link=dict(source=src, target=tgt, value=val, color="rgba(255,255,255,0.10)"),
            )
        )
        fig.update_layout(**theme.base_layout(height=460, title="Family History → Work Interference → Treatment (Sankey)"))
        st.plotly_chart(fig, use_container_width=True)

    pc = df[["family_history", "work_interfere", "benefits", "treatment"]].copy()
    pc["treatment_code"] = pc["treatment"].map({"Yes": 1, "No": 0})
    fig = go.Figure(
        go.Parcats(
            dimensions=[
                {"label": "Family History", "values": pc["family_history"]},
                {"label": "Work Interference", "values": pc["work_interfere"].astype(str)},
                {"label": "Benefits", "values": pc["benefits"]},
                {"label": "Treatment", "values": pc["treatment"]},
            ],
            line=dict(
                color=pc["treatment_code"],
                colorscale=[[0, theme.YES_NO["No"]], [1, theme.YES_NO["Yes"]]],
                shape="hspline",
            ),
        )
    )
    fig.update_layout(**theme.base_layout(height=460, title="Family History → Interference → Benefits → Treatment (Parallel Categories)"))
    st.plotly_chart(fig, use_container_width=True)

# ================================================================== MODEL PERFORMANCE
elif section == "Model Performance":
    st.markdown("## 🤖 Model Performance")
    st.caption(f"Two classifiers trained on 18 cleaned features to predict `treatment`. Best model: **{best_model_name}**.")

    theme.kpi_grid(
        [
            ("Accuracy", f"{best.accuracy * 100:.1f}%", best_model_name),
            ("ROC-AUC", f"{best.roc_auc:.3f}", "on held-out 25% test set"),
            ("Precision", f"{best.precision * 100:.1f}%", "of predicted 'Yes' correct"),
            ("Recall", f"{best.recall * 100:.1f}%", "of actual 'Yes' captured"),
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for name, res in model_results.items():
            fig.add_trace(go.Scatter(x=res.fpr, y=res.tpr, mode="lines", name=f"{name} (AUC={res.roc_auc:.3f})",
                                      line=dict(width=3, color=theme.CAT[0] if name == "Logistic Regression" else theme.CAT[2])))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random guess", line=dict(dash="dash", color=theme.TEXT_MUTED)))
        fig.update_xaxes(title="False Positive Rate")
        fig.update_yaxes(title="True Positive Rate")
        st.plotly_chart(theme.style(fig, "ROC Curve", height=420), use_container_width=True)
    with c2:
        cm = best.cm
        fig = go.Figure(
            data=go.Heatmap(
                z=cm, x=["Predicted No", "Predicted Yes"], y=["Actual No", "Actual Yes"],
                colorscale=theme.SEQUENTIAL_BLUE, text=cm, texttemplate="%{text}", showscale=False,
            )
        )
        st.plotly_chart(theme.style(fig, f"Confusion Matrix — {best_model_name}", height=420), use_container_width=True)

    rf_importance = model_results["Random Forest"].feature_importance
    if rf_importance is not None:
        fig = px.bar(
            rf_importance.sort_values("importance"), x="importance", y="feature", orientation="h",
            color_discrete_sequence=[theme.CAT[0]],
        )
        fig.update_xaxes(title="Importance")
        fig.update_yaxes(title="")
        st.plotly_chart(theme.style(fig, "Top Feature Importances (Random Forest)", height=440), use_container_width=True)

    comp = pd.DataFrame(
        [
            {"Model": name, "Accuracy": f"{r.accuracy*100:.1f}%", "ROC-AUC": f"{r.roc_auc:.3f}",
             "Precision": f"{r.precision*100:.1f}%", "Recall": f"{r.recall*100:.1f}%", "F1": f"{r.f1*100:.1f}%"}
            for name, r in model_results.items()
        ]
    )
    st.markdown("#### Model comparison")
    st.dataframe(comp, use_container_width=True, hide_index=True)

# ================================================================== TRY THE PREDICTION TOOL
elif section == "Try the Prediction Tool":
    st.markdown("## 🔮 Try the Prediction Tool")
    st.markdown(
        """
        <div class="disclaimer">
        ⚠️ <b>Educational demo only — not a diagnostic tool.</b> This predicts, from a small self-selected
        2014 survey, whether someone with similar answers <i>reported having sought treatment</i>. It cannot
        diagnose a mental health condition and should never be used to make decisions about a real person.
        If you or someone you know is struggling, please reach out to a mental health professional or a
        helpline in your country.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    with st.form("prediction_form"):
        f1, f2, f3 = st.columns(3)
        with f1:
            age = st.slider("Age", 18, 75, 30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            family_history = st.selectbox("Family history of mental illness?", ["Yes", "No"])
            work_interfere = st.selectbox("If applicable, how often does/did it interfere with work?", INTERFERE_ORDER)
        with f2:
            no_employees = st.selectbox("Company size", EMPLOYEE_ORDER)
            remote_work = st.selectbox("Work remotely ≥50% of the time?", ["Yes", "No"])
            benefits = st.selectbox("Employer provides mental health benefits?", ["Yes", "No", "Don't know"])
            care_options = st.selectbox("Aware of employer's care options?", ["Yes", "No", "Not sure"])
        with f3:
            anonymity = st.selectbox("Is anonymity protected for treatment resources?", ["Yes", "No", "Don't know"])
            leave = st.selectbox("How easy is it to take medical leave?", LEAVE_ORDER)
            supervisor = st.selectbox("Willing to discuss with your supervisor?", ["Yes", "No", "Some of them"])
            mental_health_consequence = st.selectbox("Would discussing it have negative consequences?", ["Yes", "No", "Maybe"])

        submitted = st.form_submit_button("Predict")

    if submitted:
        form_values = {
            "Age": age, "Gender": gender, "family_history": family_history, "work_interfere": work_interfere,
            "no_employees": no_employees, "remote_work": remote_work, "benefits": benefits,
            "care_options": care_options, "anonymity": anonymity, "leave": leave, "supervisor": supervisor,
            "mental_health_consequence": mental_health_consequence,
        }
        proba = predict_probability(best.pipeline, form_values, mode_row) * 100

        if proba < 34:
            color, tier = theme.CAT[2], "Lower likelihood"
        elif proba < 66:
            color, tier = theme.CAT[3], "Moderate likelihood"
        else:
            color, tier = theme.CAT[7], "Higher likelihood"

        g1, g2 = st.columns([2, 3])
        with g1:
            st.plotly_chart(theme.gauge(proba, f"{tier}", color=color), use_container_width=True)
        with g2:
            theme.content_card_open("What's driving this estimate")
            st.markdown(
                f"Based on **{best_model_name}** (test-set ROC-AUC {best.roc_auc:.3f}), respondents with a similar "
                f"profile show a **{proba:.0f}%** modeled likelihood of having sought treatment. Globally, across "
                "the whole dataset, the model relies most on:"
            )
            rf_imp = model_results["Random Forest"].feature_importance
            if rf_imp is not None:
                for _, row in rf_imp.head(5).iterrows():
                    st.markdown(f"- `{row['feature']}`")
            theme.content_card_close()

# ================================================================== RESPONSE TIMELINE
elif section == "Response Timeline":
    st.markdown("## 📈 Response Timeline")
    st.caption(
        "This is a single 2014 OSMI survey wave — there is no separate 2016 dataset provided — but responses "
        "trickled in from August 2014 through February 2016. This page explores that real collection timeline."
    )

    tdf = df.copy()
    tdf["month"] = tdf["Timestamp"].dt.to_period("M").astype(str)
    monthly = tdf.groupby("month").size().reset_index(name="count")
    monthly["cumulative"] = monthly["count"].cumsum()

    frames = [
        go.Frame(data=[go.Scatter(x=monthly["month"][: i + 1], y=monthly["cumulative"][: i + 1])], name=str(i))
        for i in range(len(monthly))
    ]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=monthly["month"][:1], y=monthly["cumulative"][:1], mode="lines+markers",
                line=dict(color=theme.ACCENT_CYAN, width=3), fill="tozeroy",
                fillcolor="rgba(56,189,248,0.15)",
            )
        ],
        frames=frames,
    )
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons", showactive=False, y=1.12, x=0,
                buttons=[
                    dict(label="▶ Play", method="animate",
                         args=[None, {"frame": {"duration": 220, "redraw": True}, "fromcurrent": True}]),
                    dict(label="⏸ Pause", method="animate",
                         args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
                ],
            )
        ],
        xaxis=dict(
            type="category", categoryorder="array", categoryarray=list(monthly["month"]),
            range=[-0.5, len(monthly) - 0.5],
        ),
        yaxis=dict(range=[0, monthly["cumulative"].max() * 1.1]),
    )
    fig.update_xaxes(title="Month")
    fig.update_yaxes(title="Cumulative Respondents")
    st.plotly_chart(theme.style(fig, "Cumulative Survey Responses Over Time (animated — press ▶ Play)", height=440), use_container_width=True)

    tdf["window"] = np.where(tdf["Timestamp"] < "2014-10-01", "Launch window (Aug–Sep 2014)", "Long tail (Oct 2014 – Feb 2016)")
    win = tdf.groupby("window").agg(respondents=("Age", "size"), treatment_rate=("treatment", lambda s: (s == "Yes").mean() * 100)).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(win, x="window", y="respondents", color="window", color_discrete_sequence=theme.CAT)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(title="")
        st.plotly_chart(theme.style(fig, "Respondents: Launch Window vs. Long Tail", height=380), use_container_width=True)
    with c2:
        fig = px.bar(win, x="window", y="treatment_rate", color="window", color_discrete_sequence=theme.CAT,
                     text=[f"{v:.1f}%" for v in win["treatment_rate"]])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        fig.update_xaxes(title="")
        fig.update_yaxes(title="Treatment Rate (%)", range=[0, 100])
        st.plotly_chart(theme.style(fig, "Treatment Rate: Launch Window vs. Long Tail", height=380), use_container_width=True)

    st.caption(
        f"96% of responses ({int(tdf['window'].eq('Launch window (Aug–Sep 2014)').sum())} of {len(tdf)}) arrived in "
        "the first six weeks after launch, typical of a single social/community-shared survey link rather than a "
        "sustained, multi-year collection effort."
    )

# ================================================================== RECOMMENDATIONS & ABOUT
elif section == "Recommendations & About":
    st.markdown("## 📌 Recommendations &amp; About")

    theme.content_card_open("What should an employer do with this?")
    st.markdown(
        """
1. **Communicate existing benefits clearly and repeatedly.** A third of respondents don't know whether benefits or care options exist — the cheapest, highest-leverage fix available.
2. **Simplify and clarify medical leave policy.** A large "don't know" group around leave difficulty suggests ambiguity itself is a quiet barrier.
3. **Target awareness campaigns at male employees specifically.** Male respondents (79% of the sample) show a meaningfully lower treatment-seeking rate.
4. **Don't wait for scale.** Company size barely moves treatment-seeking — smaller companies shouldn't deprioritize mental health support.
5. **Set realistic expectations for policy impact.** The two strongest predictors (family history, work interference) are outside an employer's direct control — benefits and communication help, but are one part of a broader system.
        """
    )
    theme.content_card_close()

    c1, c2 = st.columns(2)
    with c1:
        theme.content_card_open("Methodology & tech stack")
        st.markdown(
            """
- **Data cleaning:** invalid `Age` outliers corrected, 49 raw `Gender` values standardized into 3 categories, missing `work_interfere` treated as its own category.
- **EDA:** 20+ charts across univariate, bivariate, and multivariate views (see companion Jupyter notebook).
- **Modeling:** Logistic Regression + Random Forest, evaluated by ROC-AUC, precision, recall, and F1 on a held-out 25% test split.
- **Stack:** pandas, scikit-learn, Plotly, Streamlit.
            """
        )
        st.markdown(
            '<span class="tag">Python</span><span class="tag">pandas</span><span class="tag">scikit-learn</span>'
            '<span class="tag">Plotly</span><span class="tag">Streamlit</span>',
            unsafe_allow_html=True,
        )
        theme.content_card_close()
    with c2:
        theme.content_card_open("About")
        st.markdown(
            """
Built by **Shyam Jagani** as a data analytics internship / portfolio project, exploring the 2014 OSMI
Mental Health in Tech Survey end-to-end: cleaning, exploratory analysis, predictive modeling, and an
interactive dashboard for a non-technical audience such as an HR or People Ops team.

[LinkedIn](https://linkedin.com/in/shyam-jagani-356535141) · Dataset © Open Sourcing Mental Illness (OSMI),
used for educational/portfolio purposes.
            """
        )
        theme.content_card_close()
