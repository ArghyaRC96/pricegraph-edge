import streamlit as st
from utils.ui import inject_theme, hero, metric_card, section_header
from utils.data_loader import load_app_data, artifact_status

st.set_page_config(page_title="PriceGraph Edge", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_theme()
data = load_app_data()
hero()

recs, nodes, edges = data["recommendations"], data["nodes"], data["edges"]
products = len(nodes) if nodes is not None else 100
decisions = len(recs) if recs is not None else 999
priority = len(edges) if edges is not None else 326
connected = int((nodes["total_connections"] > 0).sum()) if nodes is not None else 90

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Pricing Products", f"{products}", "Curated pricing portfolio")
with c2: metric_card("Pricing Decisions", f"{decisions:,}", "Eligible SKU-store recommendations")
with c3: metric_card("Priority Graph Edges", f"{priority:,}", "Strong + moderate cross-price links")
with c4: metric_card("Connected Products", f"{connected}", "Products linked inside PriceGraph")

section_header("MODEL PERFORMANCE","The forecast engine earned its seat.","Final Poisson XGBoost results on the untouched 52-week holdout.")
m1,m2,m3,m4 = st.columns(4)
with m1: metric_card("R²","0.845","Untouched 52-week test")
with m2: metric_card("MAE","9.78","Mean Absolute Error")
with m3: metric_card("RMSE","21.95","Root Mean Squared Error")
with m4: metric_card("WAPE","31.38%","Weighted Absolute Percentage Error")

section_header("WORKFLOW","From raw retail history to pricing intelligence.","The app exposes the full decision pipeline without pretending observational relationships are causal.")
a,b,c = st.columns(3)
with a: metric_card("01","Predict","Poisson XGBoost estimates weekly demand.")
with b: metric_card("02","Simulate","Historically supported price scenarios are compared.")
with c: metric_card("03","Connect","Directed cross-price signals build PriceGraph.")

missing = [k for k,v in artifact_status().items() if not v]
if missing:
    st.info("UI is live. Generated model/data artifacts still need to be synced locally: " + ", ".join(missing))
