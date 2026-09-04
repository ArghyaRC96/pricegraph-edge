from pathlib import Path
import json
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS = PROJECT_ROOT / "models"

@st.cache_data
def load_csv(name):
    path = PROCESSED / name
    if not path.exists():
        return None
    return pd.read_csv(path)

@st.cache_data
def load_json(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_app_data():
    return {
        "recommendations": load_csv("portfolio_price_recommendations_enriched.csv"),
        "nodes": load_csv("pricegraph_nodes.csv"),
        "edges": load_csv("pricegraph_priority_edges.csv"),
        "neighborhoods": load_csv("pricegraph_neighborhoods.csv"),
        "weekly": load_csv("streamlit_weekly_history.csv"),
        "model_data": load_csv("simulator_context.csv"),
        "price_support": load_csv("simulator_price_support.csv"),
        "metadata": load_json(MODELS / "pricegraph_model_metadata.json"),
    }

def artifact_status():
    files = {
        "Pricing Recommendations": PROCESSED / "portfolio_price_recommendations_enriched.csv",
        "PriceGraph Nodes": PROCESSED / "pricegraph_nodes.csv",
        "PriceGraph Priority Edges": PROCESSED / "pricegraph_priority_edges.csv",
        "PriceGraph Neighborhoods": PROCESSED / "pricegraph_neighborhoods.csv",
        "XGBoost Model": MODELS / "pricegraph_xgb_poisson.json",
        "Preprocessor": MODELS / "pricegraph_preprocessor.joblib",
    }
    return {name: path.exists() for name, path in files.items()}
