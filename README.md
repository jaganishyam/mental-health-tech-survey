# 🧠 Mental Health in Tech Survey — EDA & Streamlit Dashboard

An exploratory data analysis and interactive Streamlit dashboard built on the **2014 OSMI Mental Health in Tech Survey**, examining attitudes toward mental health and the workplace factors associated with employees seeking treatment for a mental health condition.

**Live app:** _add your Streamlit Community Cloud URL here after deployment_

---

## 📌 Project Overview

Mental health is often under-discussed in fast-paced tech workplaces. This project analyzes 1,259 survey responses collected by [Open Sourcing Mental Illness (OSMI)](https://osmihelp.org/) in 2014 to answer a practical business question:

> **What demographic and workplace factors are associated with an employee seeking treatment for a mental health condition, and what should employers change to remove barriers to that treatment?**

The project has two deliverables:

| Deliverable | File | Purpose |
|---|---|---|
| EDA Notebook | `Mental_Health_Tech_Survey_EDA.ipynb` | Full data cleaning, 20 charts (Univariate/Bivariate/Multivariate), insights, and business recommendations |
| Streamlit App | `app.py` | Interactive dashboard for a non-technical audience to explore the same findings with live filters |

## 📊 Dataset

- **Source:** [OSMI Mental Health in Tech Survey (2014)](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey), `survey.csv`
- **Size:** 1,259 rows × 27 columns
- **Contents:** demographics (Age, Gender, Country, state) plus 20+ questions on workplace mental health policy, personal history, and attitudes (`treatment`, `family_history`, `work_interfere`, `benefits`, `care_options`, `leave`, `mental_health_consequence`, etc.)

### Data cleaning performed

- **Age** — invalid entries (negative values, and one value of `99999999999`) were corrected; missing/invalid ages imputed with the median.
- **Gender** — 49 inconsistent free-text values standardized into `Male` / `Female` / `Other`.
- **self_employed** — missing values (1.4%) imputed with the mode.
- **work_interfere** — missing values (20.9%, respondents without a condition) relabeled `"Not applicable"` instead of dropped.
- **state** — missing values (non-U.S. respondents) explicitly labeled rather than left null.
- **comments** — dropped (87% missing free text, not usable for structured EDA).
- **Country** — bucketed into top 10 + "Other" for readable charts (raw column preserved).
- **no_employees / work_interfere / leave** — converted to ordered categoricals so charts display in logical order.

The same cleaning logic lives in `utils.py` (used by the Streamlit app) and is reproduced inline in the notebook, so both deliverables agree.

## 🔍 Key Findings

1. **Family history of mental illness** is the strongest single predictor of treatment-seeking (~74% vs. ~35% treatment rate).
2. **Work interference severity** shows a near dose-response relationship with treatment-seeking — respondents reporting frequent interference sought treatment at over 90%.
3. **Awareness**, not just existence, of mental health benefits and care options tracks closely with who actually seeks treatment — roughly a third of respondents don't know what their employer offers.
4. **Male respondents** seek treatment at a meaningfully lower rate than Female/Other respondents despite being the majority of the sample.
5. **Company size** and **remote-work status** show little relationship with treatment-seeking.
6. **Age** has almost no relationship with treatment-seeking — support should be designed for the whole workforce, not one age band.

Full reasoning, charts, and business recommendations are in the notebook's *Solution to Business Objective* and *Conclusion* sections.

## 🖥️ Streamlit App

The dashboard has six sections, all responsive to sidebar filters (Gender, Age range, Country, Company size):

- **Overview** — headline KPIs and treatment split
- **Demographics** — age, gender, and age-by-gender breakdowns
- **Workplace Factors** — company size, remote work, benefits, care options, leave policy
- **Treatment Analysis** — pick any factor and compare treatment-seeking counts and rate
- **Correlation Explorer** — heatmap of encoded features + ranked correlation with `treatment`
- **Explore the Data** — filterable raw table with CSV export

## 📁 Project Structure

```
mental-health-tech-survey/
├── app.py                              # Streamlit dashboard
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

## ⚙️ Running Locally

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

The app opens automatically at `http://localhost:8501`.

To run the notebook: `jupyter notebook Mental_Health_Tech_Survey_EDA.ipynb` (or open it in JupyterLab / VS Code / Google Colab).

## 🚀 Deploying to Streamlit Community Cloud

1. **Push this project to GitHub.**
   ```bash
   git init
   git add .
   git commit -m "Mental Health in Tech Survey - EDA and Streamlit app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/mental-health-tech-survey.git
   git push -u origin main
   ```
   Make sure `data/survey.csv` is committed (it's small enough to keep in the repo — do **not** add it to `.gitignore`).

2. **Sign in to Streamlit Community Cloud** at [share.streamlit.io](https://share.streamlit.io) using your GitHub account (the same one hosting this repo).

3. **Click "Create app"** → choose **"Deploy a public app from GitHub"**.

4. **Fill in the deploy form:**
   - **Repository:** `<your-username>/mental-health-tech-survey`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - (Optional) Pick a custom subdomain under "App URL" — this becomes `https://<subdomain>.streamlit.app`

5. **Click "Deploy".** Streamlit Cloud installs everything listed in `requirements.txt` automatically and starts the app. The first deploy typically takes 1–3 minutes.

6. **Every future `git push` to `main` automatically redeploys the app** — no manual redeploy step needed.

7. Once live, copy the app's URL back into this README's "Live app" line at the top, and into your GitHub repo description, so anyone reviewing your portfolio can open it directly.

### Troubleshooting deployment

- **"ModuleNotFoundError"** → the missing package isn't in `requirements.txt`; add it and push again.
- **App shows "Error running app" on data load** → confirm `data/survey.csv` was actually pushed to GitHub (check the repo on github.com) and that the path in `utils.py` (`data/survey.csv`) matches the repo's folder structure exactly.
- **App sleeps after inactivity** → free-tier Streamlit Community Cloud apps go to sleep after a period with no visitors; the next visitor simply triggers a ~30 second wake-up, no action needed.

## 🛠️ Tech Stack

- **Python** — pandas, numpy for data cleaning and analysis
- **Matplotlib / Seaborn** — static charts in the EDA notebook
- **Plotly** — interactive charts in the Streamlit app
- **Streamlit** — dashboard framework and hosting (Streamlit Community Cloud)

## 👤 Author

**Shyam Jagani**
[LinkedIn](https://linkedin.com/in/shyam-jagani-356535141)

---

*Built as part of a data analytics internship project. Dataset © Open Sourcing Mental Illness (OSMI), used under its original license for educational/portfolio purposes.*
