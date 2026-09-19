# data loading + cleaning, shared between the app and (in spirit) the notebook
import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = "data/survey.csv"

EMPLOYEE_ORDER = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
INTERFERE_ORDER = ["Never", "Rarely", "Sometimes", "Often", "Not applicable"]
LEAVE_ORDER = ["Very easy", "Somewhat easy", "Don't know", "Somewhat difficult", "Very difficult"]
AGE_BINS = [17, 24, 34, 44, 54, 100]
AGE_LABELS = ["18-24", "25-34", "35-44", "45-54", "55+"]

FEMALE_VALUES = {
    "female", "f", "woman", "femake", "femail", "cis female",
    "cis-female/femme", "female (cis)", "female (trans)", "woman ",
}
MALE_VALUES = {
    "male", "m", "man", "mal", "maile", "make", "msle", "mail", "malr",
    "cis male", "cis man", "male (cis)", "male-ish", "male leaning androgynous",
    "guy (-ish) ^_^", "ostensibly male, unsure what that really means",
}


def _standardize_gender(g: str) -> str:
    g = str(g).strip().lower()
    if g in FEMALE_VALUES:
        return "Female"
    if g in MALE_VALUES:
        return "Male"
    return "Other"


@st.cache_data(show_spinner="loading data...")
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    # same cleaning steps as the notebook, kept here so the app doesn't need to re-run it
    df = pd.read_csv(path)
    df = df.copy()

    # --- Age: fix invalid entries ---
    invalid_age_mask = (df["Age"] < 15) | (df["Age"] > 100)
    df.loc[invalid_age_mask, "Age"] = np.nan
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Age"] = df["Age"].astype(int)
    df["age_group"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS)

    # --- Gender: standardize ---
    df["Gender"] = df["Gender"].apply(_standardize_gender)

    # --- self_employed: impute with mode ---
    df["self_employed"] = df["self_employed"].fillna(df["self_employed"].mode()[0])

    # --- work_interfere: explicit "Not applicable" ---
    df["work_interfere"] = df["work_interfere"].fillna("Not applicable")

    # --- state: label non-US clearly ---
    df["state"] = df["state"].fillna("Not Applicable (Non-US)")

    # --- comments: drop (87% missing free text) ---
    if "comments" in df.columns:
        df = df.drop(columns=["comments"])

    # --- Timestamp ---
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # --- Country grouping ---
    top_countries = df["Country"].value_counts().nlargest(10).index
    df["country_grouped"] = df["Country"].where(df["Country"].isin(top_countries), "Other")

    # --- Ordered categoricals ---
    df["no_employees"] = pd.Categorical(df["no_employees"], categories=EMPLOYEE_ORDER, ordered=True)
    df["work_interfere"] = pd.Categorical(df["work_interfere"], categories=INTERFERE_ORDER, ordered=True)
    df["leave"] = pd.Categorical(df["leave"], categories=LEAVE_ORDER, ordered=True)

    return df


def encode_for_correlation(df: pd.DataFrame) -> pd.DataFrame:
    # turns the Yes/No/Don't know style columns into numbers so corr() works
    cols = [
        "Age", "family_history", "treatment", "work_interfere", "remote_work",
        "benefits", "care_options", "wellness_program", "seek_help", "anonymity",
        "mental_health_consequence", "supervisor", "obs_consequence",
    ]
    enc = df[cols].copy()

    binary_map = {"Yes": 1, "No": 0}
    for col in ["family_history", "treatment", "remote_work", "obs_consequence"]:
        enc[col] = enc[col].map(binary_map)

    interfere_map = {"Never": 0, "Rarely": 1, "Not applicable": 1, "Sometimes": 2, "Often": 3}
    enc["work_interfere"] = enc["work_interfere"].astype(str).map(interfere_map)

    three_map = {"No": 0, "Don't know": 1, "Yes": 2}
    for col in ["benefits", "care_options", "wellness_program", "seek_help", "anonymity"]:
        enc[col] = enc[col].map(three_map)

    consequence_map = {"No": 0, "Maybe": 1, "Yes": 2}
    enc["mental_health_consequence"] = enc["mental_health_consequence"].map(consequence_map)

    supervisor_map = {"No": 0, "Some of them": 1, "Yes": 2}
    enc["supervisor"] = enc["supervisor"].map(supervisor_map)

    return enc


SUPPORT_FACTORS = {
    "benefits": {"No": 0, "Don't know": 1, "Yes": 2},
    "care_options": {"No": 0, "Not sure": 1, "Yes": 2},
    "wellness_program": {"No": 0, "Don't know": 1, "Yes": 2},
    "seek_help": {"No": 0, "Don't know": 1, "Yes": 2},
    "anonymity": {"No": 0, "Don't know": 1, "Yes": 2},
    "leave": {"Very difficult": 0, "Somewhat difficult": 1, "Don't know": 1, "Somewhat easy": 2, "Very easy": 3},
}


def workplace_support_index(df: pd.DataFrame) -> pd.DataFrame:
    # scores each factor 0-100, split by treatment Yes/No - feeds the radar chart
    rows = []
    for factor, mapping in SUPPORT_FACTORS.items():
        max_score = max(mapping.values())
        scored = df[factor].astype(str).map(mapping)
        for outcome in ["Yes", "No"]:
            subset = scored[df["treatment"] == outcome]
            avg_pct = (subset.mean() / max_score) * 100 if max_score else 0
            rows.append({"factor": factor, "treatment": outcome, "score": avg_pct})
    return pd.DataFrame(rows)
