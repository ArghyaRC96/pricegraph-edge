from pathlib import Path
import sys
STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import streamlit as st
import plotly.graph_objects as go
from utils.ui import inject_theme, page_header, metric_card, section_header, artifact_missing
from utils.data_loader import load_app_data

st.set_page_config(page_title="Product Explorer", page_icon="P", layout="wide")
inject_theme()
page_header("PRODUCT INTELLIGENCE","Product Explorer","Open any product and inspect its commercial profile, store-level pricing decisions, and PriceGraph connectivity.")
data = load_app_data()
nodes, recs, neigh = data["nodes"], data["recommendations"], data["neighborhoods"]

if nodes is None:
    artifact_missing(["pricegraph_nodes.csv"])
    st.stop()

item = st.selectbox("Select product", sorted(nodes["item_id"].unique().tolist()))
node = nodes[nodes["item_id"] == item].iloc[0]
item_recs = recs[recs["item_id"] == item].copy() if recs is not None else None
item_neigh = neigh[neigh["item_id"] == item].copy() if neigh is not None else None

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Department", str(node["dept_id"]), "Anonymized M5 department")
with c2: metric_card("Total Units", f'{int(node["total_units"]):,}', "Historical portfolio units")
with c3: metric_card("Connections", f'{int(node["total_connections"])}', "Priority PriceGraph links")
with c4: metric_card("Strong Links", f'{int(node["total_strong_connections"])}', "Strong evidence tier")

if item_recs is not None and len(item_recs):
    section_header("STORE PRICING","Current vs recommended prices.","Model-based recommendation snapshot by store.")
    fig = go.Figure()
    fig.add_bar(name="Current", x=item_recs["store_id"], y=item_recs["current_price"], marker_color="#B7C0D5")
    fig.add_bar(name="Recommended", x=item_recs["store_id"], y=item_recs["recommended_price"], marker_color="#6C5CE7")
    fig.update_layout(barmode="group", height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.55)",
                      xaxis_title="Store", yaxis_title="Price", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
    view = ["store_id","current_price","recommended_price","price_change_pct","predicted_revenue_gain_pct","recommendation_reliability"]
    st.dataframe(item_recs[view].sort_values("predicted_revenue_gain_pct", ascending=False), use_container_width=True, hide_index=True)
else:
    artifact_missing(["portfolio_price_recommendations_enriched.csv"])

section_header("PRICEGRAPH PROFILE","How this product connects to the portfolio.","Incoming means neighbor price -> selected product demand. Outgoing means selected product price -> neighbor demand.")
if item_neigh is not None and len(item_neigh):
    cols = ["neighbor_item","edge_direction","relationship_type","edge_strength","cross_price_corr","price_change_events"]
    st.dataframe(item_neigh[cols].head(15), use_container_width=True, hide_index=True)
else:
    st.info("No priority PriceGraph neighborhood is available for this product.")
