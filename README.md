# Mental Health in Tech Survey — EDA & Streamlit Dashboard

Exploratory data analysis and a Streamlit dashboard built on the **2014 OSMI Mental Health in Tech Survey**, looking at attitudes toward mental health in the workplace and what's associated with an employee seeking treatment.

**Live app:** _add your Streamlit Community Cloud URL here after deployment_

---

## Project overview

Mental health tends to be under-discussed in tech workplaces. This project works through 1,259 survey responses collected by [Open Sourcing Mental Illness (OSMI)](https://osmihelp.org/) in 2014 to answer one question:

> What demographic and workplace factors are associated with an employee seeking treatment for a mental health condition, and what should employers change to remove barriers to that treatment?

Two deliverables:

| Deliverable | File(s) | Purpose |
|---|---|---|
| EDA notebook | `Mental_Health_Tech_Survey_EDA.ipynb` | Data cleaning, 20 charts across univariate/bivariate/multivariate views, findings, and recommendations |
| Streamlit app | `app.py`, `theme.py`, `model.py`, `utils.py` | An interactive dashboard covering the same EDA, plus two trained classifiers to see which factors actually predict treatment-seeking |

## Dataset

- **Source:** [OSMI Mental Health in Tech Survey (2014)](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey), `survey.csv`
- **Size:** 1,259 rows × 27 columns
- **Contents:** demographics (Age, Gender, Country, state) plus 20+ questions on workplace mental health policy, personal history, and attitudes (`treatment`, `family_history`, `work_interfere`, `benefits`, `care_options`, `leave`, `mental_health_consequence`, etc.)

### Data cleaning

- **Age** — invalid entries (negative values, one value of `99999999999`) corrected; missing/invalid ages imputed with the median.
- **Gender** — 49 inconsistent free-text values standardized into `Male` / `Female` / `Other`.
- **self_employed** — missing values (1.4%) imputed with the mode.
- **work_interfere** — missing values (20.9%, mostly respondents without a condition) relabeled `"Not applicable"` instead of dropped.
- **state** — missing values (non-U.S. respondents) explicitly labeled rather than left null.
- **comments** — dropped (87% missing free text, not useful for structured EDA).
- **Country** — bucketed into top 10 + "Other" for readable charts (raw column kept).
- **no_employees / work_interfere / leave** — converted to ordered categoricals so charts display in logical order.

The cleaning logic lives in `utils.py` and is reproduced inline in the notebook, so the app and the notebook agree on the data.

## Key findings

1. **Family history of mental illness** is the strongest single predictor of treatment-seeking (~74% vs. ~35% treatment rate).
2. **Work interference severity** has a near dose-response relationship with treatment-seeking — respondents reporting frequent interference sought treatment at over 90%.
3. **Awareness** of mental health benefits and care options (not just whether they exist) tracks closely with who seeks treatment — roughly a third of respondents don't know what their employer offers.
4. **Male respondents** seek treatment at a meaningfully lower rate than Female/Other respondents, despite being the majority of the sample.
5. **Company size** and **remote-work status** show little relationship with treatment-seeking.
6. **Age** has almost no relationship with treatment-seeking — support should be designed for the whole workforce, not one age band.

Full reasoning, charts, and recommendations are in the notebook's *Solution to Business Objective* and *Conclusion* sections.

## Streamlit app

A dark dashboard themed around green — the color generally associated with mental health awareness — with navigation as buttons across the top of the main page rather than a sidebar. Six pages:

- **Overview** — KPI cards (respondents, treatment rate, best model ROC-AUC, top predictor), project story, and key findings.
- **Explore & Segment** — filters for Gender, Age, Country, and Company size, plus a violin plot (Age by treatment), a sunburst (Gender → Family History → Treatment), a treemap (Country → Company Size), and a bubble chart (Country: age vs. treatment rate vs. sample size).
- **Correlations & Drivers** — a correlation heatmap, a ranked correlation bar, a radar chart comparing a "workplace support index" between those who sought treatment and those who didn't, a Sankey diagram (Family History → Work Interference → Treatment), and a parallel categories diagram tracing four factors at once.
- **Model Performance** — Logistic Regression and Random Forest, compared by accuracy, ROC-AUC, precision, recall, and F1, with an ROC curve, confusion matrix, and feature-importance chart. This page shows how the models perform, not a form to try them yourself.
- **Response Timeline** — an animated (play/pause) cumulative-responses chart from the real survey timestamps (Aug 2014 – Feb 2016), plus a launch-window vs. long-tail comparison. This is one survey wave with a long tail of late responses, not a separate 2016 dataset — the page says so.
- **Recommendations & About** — recommendations, methodology/tech stack, and author info.

The chart colors are a fixed, colorblind-checked palette (kept the same regardless of theme changes, since that's an accessibility concern separate from branding) — only the surrounding UI chrome (headers, cards, buttons) uses the green accent.

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
│   └── config.toml                     # App theme (base Streamlit chrome)
├── .gitignore
└── README.md
```

## Running locally

```bash
# 1. Clone your repository
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

To run the notebook: `jupyter notebook Mental_Health_Tech_Survey_EDA.ipynb` (or open it in JupyterLab, VS Code, or Google Colab).

## Deploying to Streamlit Community Cloud

1. **Push this project to GitHub.**
   ```bash
   git init
   git add .
   git commit -m "Mental Health in Tech Survey - EDA and Streamlit app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/mental-health-tech-survey.git
   git push -u origin main
   ```
   Make sure `data/survey.csv` is committed (it's small enough to keep in the repo — don't add it to `.gitignore`).

2. **Sign in to Streamlit Community Cloud** at [share.streamlit.io](https://share.streamlit.io) with your GitHub account (the one hosting this repo).

3. **Click "Create app"** → **"Deploy a public app from GitHub"**.

4. **Fill in the deploy form:**
   - **Repository:** `<your-username>/mental-health-tech-survey`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - (Optional) pick a custom subdomain under "App URL" — this becomes `https://<subdomain>.streamlit.app`

5. **Click "Deploy".** Streamlit Cloud installs everything in `requirements.txt` and starts the app. First deploy usually takes 1–3 minutes.

6. **Every push to `main` redeploys the app automatically** — no manual step needed.

7. Once live, put the app's URL back into this README's "Live app" line and into your GitHub repo description.

### Troubleshooting deployment

- **"ModuleNotFoundError"** — the missing package isn't in `requirements.txt`; add it and push again.
- **App shows "Error running app" on data load** — confirm `data/survey.csv` was pushed to GitHub and that the path in `utils.py` (`data/survey.csv`) matches the repo structure exactly.
- **App sleeps after inactivity** — free-tier Streamlit Community Cloud apps go to sleep with no visitors; the next visitor triggers a ~30 second wake-up, nothing to fix.

## Tech stack

- **Python** — pandas, numpy for data cleaning and analysis
- **Matplotlib / Seaborn** — static charts in the EDA notebook
- **Plotly** — interactive charts in the Streamlit app (violin, sunburst, treemap, bubble, radar, Sankey, parallel categories, animated timeline)
- **scikit-learn** — Logistic Regression and Random Forest, evaluation metrics
- **Streamlit** — dashboard framework and hosting (Streamlit Community Cloud)
- **Custom CSS** (`theme.py`) — dark theme, cards, nav buttons

## Author

**Shyam Jagani**
[LinkedIn](https://linkedin.com/in/shyam-jagani-356535141)

---

*Built as part of a data analytics internship project. Dataset © Open Sourcing Mental Illness (OSMI), used under its original license for educational/portfolio purposes.*
