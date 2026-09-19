# Mental Health in Tech Survey — EDA & Streamlit Dashboard

An exploratory data analysis and Streamlit dashboard built on the **2014 OSMI Mental Health in Tech Survey**, looking at how workplace factors and demographics line up with an employee seeking treatment for a mental health condition.

**Live app:** [mental-health-tech-survey-shyamjagani.streamlit.app](https://mental-health-tech-survey-shyamjagani.streamlit.app)

---

## What this is

Mental health doesn't get talked about much in tech workplaces, even though the industry has a reputation for burnout. I used the 2014 OSMI survey (1,259 responses collected by [Open Sourcing Mental Illness](https://osmihelp.org/)) to try to answer one question:

> What demographic and workplace factors are associated with an employee seeking treatment for a mental health condition, and what should employers change to remove barriers to that treatment?

There's an EDA notebook (`Mental_Health_Tech_Survey_EDA.ipynb`) that walks through the data cleaning and 20 charts across univariate, bivariate, and multivariate views, and a Streamlit app (`app.py`, `theme.py`, `model.py`, `utils.py`) that covers the same ground interactively, plus two trained classifiers to see which factors actually predict treatment-seeking.

## Dataset

- **Source:** [OSMI Mental Health in Tech Survey (2014)](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey), `survey.csv`
- **Size:** 1,259 rows × 27 columns
- **Contents:** demographics (Age, Gender, Country, state) plus 20+ questions on workplace mental health policy, personal history, and attitudes (`treatment`, `family_history`, `work_interfere`, `benefits`, `care_options`, `leave`, `mental_health_consequence`, etc.)

### Cleaning it up

The raw file needed a fair bit of work before it was usable:

- **Age** — some entries were obviously broken (negative numbers, one row with `99999999999`), so I corrected those and filled missing/invalid ages with the median.
- **Gender** — 49 inconsistent free-text values got standardized into `Male` / `Female` / `Other`.
- **self_employed** — the small number of missing values (1.4%) filled with the mode.
- **work_interfere** — missing values (20.9%, mostly people without a condition) relabeled `"Not applicable"` instead of dropped.
- **state** — missing values (non-U.S. respondents) explicitly labeled instead of left null.
- **comments** — dropped entirely (87% missing free text, not much use for structured EDA).
- **Country** — bucketed into the top 10 plus "Other" so charts stay readable.
- **no_employees / work_interfere / leave** — converted to ordered categoricals so they display in a logical order rather than alphabetically.

The cleaning logic lives in `utils.py` and is reproduced in the notebook, so the app and the notebook are working off the same data.

## What I found

1. **Family history of mental illness** is the strongest single predictor of treatment-seeking (~74% vs. ~35% treatment rate).
2. **Work interference severity** has a near dose-response relationship with treatment-seeking — people reporting frequent interference sought treatment at over 90%.
3. **Awareness** of mental health benefits and care options (not just whether they exist) tracks closely with who actually seeks treatment — about a third of respondents don't know what their employer offers.
4. **Male respondents** seek treatment at a noticeably lower rate than Female/Other respondents, despite being the majority of the sample.
5. **Company size** and **remote-work status** barely move the needle on treatment-seeking.
6. **Age** has almost no relationship with treatment-seeking, which suggests support should be designed for the whole workforce rather than one age band.

The full reasoning and recommendations are in the notebook's *Solution to Business Objective* and *Conclusion* sections.

## The Streamlit app

A green-themed dashboard (green being the color generally tied to mental health awareness) with navigation as buttons across the top of the page instead of a sidebar. Six pages:

- **Overview** — KPI cards (respondents, treatment rate, best model ROC-AUC, top predictor), a project summary, and the key findings.
- **Explore & Segment** — filters for Gender, Age, Country, and Company size, plus a violin plot (Age by treatment), a sunburst (Gender → Family History → Treatment), a treemap (Country → Company Size), and a bubble chart (Country: age vs. treatment rate vs. sample size).
- **Correlations & Drivers** — a correlation heatmap, a ranked correlation bar, a radar chart comparing a "workplace support index" between those who sought treatment and those who didn't, a Sankey diagram (Family History → Work Interference → Treatment), and a parallel categories diagram tracing four factors at once.
- **Model Performance** — Logistic Regression and Random Forest, compared by accuracy, ROC-AUC, precision, recall, and F1, with an ROC curve, confusion matrix, and feature-importance chart.
- **Response Timeline** — an animated cumulative-responses chart from the real survey timestamps (Aug 2014 – Feb 2016), plus a launch-window vs. long-tail comparison.
- **Recommendations & About** — recommendations, methodology/tech stack, and author info.

The chart colors themselves are a fixed, colorblind-checked palette that stayed the same through every theme change, since that's an accessibility concern separate from branding — only the surrounding UI (headers, cards, buttons) uses the green.

## Project structure

```
mental-health-tech-survey/
├── app.py                              # Streamlit dashboard (6 pages)
├── theme.py                            # Theme CSS, color palette, chart styling helpers
├── model.py                            # ML pipeline: training and evaluation
├── utils.py                            # Shared data loading & cleaning
├── Mental_Health_Tech_Survey_EDA.ipynb # Full EDA notebook (20 charts)
├── data/
│   └── survey.csv                      # Raw dataset
├── requirements.txt                    # Python dependencies
├── .streamlit/
│   └── config.toml                     # App theme
├── .gitignore
└── README.md
```

## Running it locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/mental-health-tech-survey.git
cd mental-health-tech-survey

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

To look at the notebook: `jupyter notebook Mental_Health_Tech_Survey_EDA.ipynb` (or open it in JupyterLab, VS Code, or Colab).

## Tech stack

- **Python** — pandas, numpy for data cleaning and analysis
- **Matplotlib / Seaborn** — static charts in the EDA notebook
- **Plotly** — interactive charts in the Streamlit app (violin, sunburst, treemap, bubble, radar, Sankey, parallel categories, animated timeline)
- **scikit-learn** — Logistic Regression and Random Forest, evaluation metrics
- **Streamlit** — dashboard framework and hosting
- **Custom CSS** (`theme.py`) — theme, cards, nav buttons

## Author

**Shyam Jagani**
[LinkedIn](https://linkedin.com/in/shyam-jagani-356535141)

---

*Built as part of a data analytics internship project. Dataset © Open Sourcing Mental Illness (OSMI), used under its original license for educational/portfolio purposes.*
