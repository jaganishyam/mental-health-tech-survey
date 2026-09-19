# trains the two classifiers used on the Model Performance page.
# nothing here is meant to diagnose anything - it's just predicting
# whether the survey answer for `treatment` was Yes or No.

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["Age"]
CATEGORICAL_FEATURES = [
    "Gender", "family_history", "work_interfere", "no_employees", "remote_work",
    "tech_company", "benefits", "care_options", "wellness_program", "seek_help",
    "anonymity", "leave", "mental_health_consequence", "coworkers", "supervisor",
    "mental_vs_physical", "obs_consequence", "country_grouped",
]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "treatment"

# used to turn one-hot column names back into something readable for
# the feature importance chart, e.g. work_interfere_Often -> "Work
# Interference Level" instead of the raw encoded name.
PRETTY_NAMES = {
    "Age": "Age",
    "Gender": "Gender",
    "family_history": "Family History of Mental Illness",
    "work_interfere": "Work Interference Level",
    "no_employees": "Company Size",
    "remote_work": "Remote Work",
    "tech_company": "Tech Company",
    "benefits": "Mental Health Benefits",
    "care_options": "Care Options Awareness",
    "wellness_program": "Wellness Program",
    "seek_help": "Seek-Help Resources",
    "anonymity": "Anonymity Protection",
    "leave": "Ease of Taking Leave",
    "mental_health_consequence": "Mental Health Consequence Concern",
    "coworkers": "Coworker Willingness",
    "supervisor": "Supervisor Willingness",
    "mental_vs_physical": "Mental vs. Physical Health Parity",
    "obs_consequence": "Observed Consequences",
    "country_grouped": "Country",
}
_RAW_COLUMNS_BY_LENGTH = sorted(ALL_FEATURES, key=len, reverse=True)  # longest first so partial matches don't win


def _raw_column(encoded_name):
    for raw_col in _RAW_COLUMNS_BY_LENGTH:
        if encoded_name == raw_col or encoded_name.startswith(raw_col + "_"):
            return raw_col
    return encoded_name


def feature_display_name(encoded_name):
    raw_col = _raw_column(encoded_name)
    return PRETTY_NAMES.get(raw_col, raw_col.replace("_", " ").title())


@dataclass
class ModelResult:
    name: str
    pipeline: object
    accuracy: float
    roc_auc: float
    precision: float
    recall: float
    f1: float
    fpr: np.ndarray
    tpr: np.ndarray
    cm: np.ndarray
    feature_importance: pd.DataFrame = field(default=None)


def _build_pipeline(estimator):
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])
    return Pipeline([("preprocess", preprocessor), ("model", estimator)])


def _evaluate(pipeline, X_test, y_test, name):
    proba = pipeline.predict_proba(X_test)[:, 1]
    preds = pipeline.predict(X_test)
    fpr, tpr, _ = roc_curve(y_test, proba)

    importance_df = None
    model = pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        feature_names = pipeline.named_steps["preprocess"].get_feature_names_out()
        raw = pd.DataFrame({"feature": feature_names, "importance": model.feature_importances_})
        raw["feature"] = raw["feature"].str.replace("cat__", "", regex=False).str.replace("num__", "", regex=False)
        # one-hot splits each question into several columns (one per answer choice),
        # so we sum importances back up per question or the chart just shows duplicates
        raw["raw_column"] = raw["feature"].apply(_raw_column)
        importance_df = (
            raw.groupby("raw_column", as_index=False)["importance"].sum()
            .sort_values("importance", ascending=False)
            .head(10)
        )
        importance_df["feature"] = importance_df["raw_column"].apply(feature_display_name)
        importance_df = importance_df[["feature", "importance"]]

    return ModelResult(
        name=name,
        pipeline=pipeline,
        accuracy=accuracy_score(y_test, preds),
        roc_auc=roc_auc_score(y_test, proba),
        precision=precision_score(y_test, preds, pos_label=1),
        recall=recall_score(y_test, preds, pos_label=1),
        f1=f1_score(y_test, preds, pos_label=1),
        fpr=fpr,
        tpr=tpr,
        cm=confusion_matrix(y_test, preds),
        feature_importance=importance_df,
    )


@st.cache_resource(show_spinner="training models...")
def train_models(df):
    data = df.copy()
    data[TARGET] = data[TARGET].map({"Yes": 1, "No": 0})
    # these three columns are pandas Categorical dtype from utils.py, sklearn wants plain strings
    data["work_interfere"] = data["work_interfere"].astype(str)
    data["no_employees"] = data["no_employees"].astype(str)
    data["leave"] = data["leave"].astype(str)

    X = data[ALL_FEATURES]
    y = data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    results = {}

    log_reg = _build_pipeline(LogisticRegression(max_iter=1000))
    log_reg.fit(X_train, y_train)
    results["Logistic Regression"] = _evaluate(log_reg, X_test, y_test, "Logistic Regression")

    rf = _build_pipeline(RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42, class_weight="balanced"))
    rf.fit(X_train, y_train)
    results["Random Forest"] = _evaluate(rf, X_test, y_test, "Random Forest")

    best_name = max(results, key=lambda k: results[k].roc_auc)
    return results, best_name
