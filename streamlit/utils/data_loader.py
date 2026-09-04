from pathlib import Path
import json

import pandas as pd
import streamlit as st

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
MODELS = PROJECT_ROOT / "models"


CATEGORICAL_FEATURES = [
    "item_id",
    "dept_id",
    "store_id",
    "state_id"
]


NUMERIC_FEATURES = [
    "sell_price",
    "price_change_pct",
    "price_vs_normal_pct",
    "price_vs_hist_mean_pct",
    "price_down_flag",
    "price_up_flag",
    "lag_1_units",
    "lag_4_units",
    "lag_13_units",
    "lag_52_units",
    "rolling_4_units",
    "rolling_13_units",
    "hist_mean_units",
    "hist_median_units",
    "lag_1_vs_mean",
    "lag_4_vs_mean",
    "lag_13_vs_mean",
    "lag_52_vs_mean",
    "rolling_4_vs_mean",
    "rolling_13_vs_mean",
    "snap_days",
    "event_days",
    "sporting_flag",
    "cultural_flag",
    "religious_flag",
    "national_flag",
    "month",
    "day_of_month",
    "week_of_year"
]


CHAMPION_FEATURES = (
    CATEGORICAL_FEATURES
    + NUMERIC_FEATURES
)


def load_csv(filename):

    path = PROCESSED_DATA / filename

    if not path.exists():
        return None

    return pd.read_csv(path)


@st.cache_data
def load_json(filename):

    path = PROCESSED_DATA / filename

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


@st.cache_data
def load_model_metadata():

    path = (
        MODELS
        / "pricegraph_model_metadata.json"
    )

    if not path.exists():
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


@st.cache_resource
def load_model_assets():

    model_path = (
        MODELS
        / "pricegraph_xgb_poisson.json"
    )

    context_path = (
        PROCESSED_DATA
        / "simulation_context.csv"
    )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Missing model: {model_path}"
        )

    if not context_path.exists():
        raise FileNotFoundError(
            f"Missing context: {context_path}"
        )


    # --------------------------------------------------------
    # LOAD XGBOOST MODEL
    # --------------------------------------------------------

    model = XGBRegressor()

    model.load_model(
        str(model_path)
    )


    # --------------------------------------------------------
    # REBUILD PREPROCESSOR LOCALLY
    #
    # This avoids sklearn/joblib version incompatibility.
    # OneHotEncoder learns categories from the complete
    # deployment context.
    # --------------------------------------------------------

    context = pd.read_csv(
        context_path
    )


    for column in CATEGORICAL_FEATURES:

        context[column] = (
            context[column]
            .astype(str)
        )


    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True
                ),
                CATEGORICAL_FEATURES
            ),
            (
                "numeric",
                "passthrough",
                NUMERIC_FEATURES
            )
        ],
        remainder="drop"
    )


    preprocessor.fit(
        context[
            CHAMPION_FEATURES
        ]
    )


    # --------------------------------------------------------
    # VALIDATE FEATURE DIMENSION AGAINST XGBOOST
    # --------------------------------------------------------

    sample = (
        context[
            CHAMPION_FEATURES
        ]
        .head(1)
        .copy()
    )


    transformed = (
        preprocessor.transform(
            sample
        )
    )


    transformed_features = (
        transformed.shape[1]
    )


    model_features = (
        model.n_features_in_
    )


    if (
        transformed_features
        != model_features
    ):

        raise ValueError(
            "Preprocessor/model feature mismatch. "
            f"Preprocessor={transformed_features}, "
            f"XGBoost={model_features}"
        )


    metadata = load_model_metadata()

    metadata["features"] = (
        CHAMPION_FEATURES
    )

    metadata["categorical_features"] = (
        CATEGORICAL_FEATURES
    )

    metadata["numeric_features"] = (
        NUMERIC_FEATURES
    )


    return (
        model,
        preprocessor,
        metadata
    )


def load_app_data():

    return {
        "recommendations":
            load_csv(
                "portfolio_price_recommendations_enriched.csv"
            ),

        "nodes":
            load_csv(
                "pricegraph_nodes.csv"
            ),

        "edges":
            load_csv(
                "pricegraph_priority_edges.csv"
            ),

        "neighborhoods":
            load_csv(
                "pricegraph_neighborhoods.csv"
            ),

        "simulation_context":
            load_csv(
                "simulation_context.csv"
            ),

        "supported_prices":
            load_csv(
                "supported_price_candidates.csv"
            ),

        "ripple_models":
            load_csv(
                "cross_price_ripple_models_production.csv"
            ),

        "scenario_policy":
            load_json(
                "scenario_policy.json"
            )
    }


def artifact_status():

    required = {
        "Simulation Context":
            PROCESSED_DATA
            / "simulation_context.csv",

        "Supported Prices":
            PROCESSED_DATA
            / "supported_price_candidates.csv",

        "Pricing Recommendations":
            PROCESSED_DATA
            / "portfolio_price_recommendations_enriched.csv",

        "PriceGraph Nodes":
            PROCESSED_DATA
            / "pricegraph_nodes.csv",

        "PriceGraph Edges":
            PROCESSED_DATA
            / "pricegraph_priority_edges.csv",

        "Ripple Models":
            PROCESSED_DATA
            / "cross_price_ripple_models_production.csv",

        "XGBoost Model":
            MODELS
            / "pricegraph_xgb_poisson.json"
    }


    return {
        name: path.exists()
        for name, path
        in required.items()
    }