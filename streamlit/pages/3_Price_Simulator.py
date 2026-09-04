from pathlib import Path
import sys
STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import streamlit as st
import plotly.graph_objects as go
from utils.ui import inject_theme, page_header, metric_card, section_header, artifact_missing
from utils.data_loader import load_app_data

st.set_page_config(page_title="Price Simulator", page_icon="🧪", layout="wide")
inject_theme()
page_header("SUPPORTED PRICE SCENARIOS","Price Simulator","Compare the saved current-price scenario with the model-selected historically supported recommendation.")
data = load_app_data()
recs = data["recommendations"]

if recs is None:
    artifact_missing(["portfolio_price_recommendations_enriched.csv"])
    section_header("ENGINE READY","Full interactive simulation comes next.","The notebook model already contains the safe candidate-price engine. Once model artifacts are synced locally, this page can evaluate every supported candidate live.")
    st.stop()

item = st.selectbox("Product", sorted(recs["item_id"].unique().tolist()))
stores = sorted(recs.loc[recs["item_id"] == item, "store_id"].unique().tolist())
store = st.selectbox("Store", stores)
row = recs[(recs["item_id"] == item) & (recs["store_id"] == store)].iloc[0]

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Current Price", f'${row["current_price"]:.2f}', "Observed current scenario")
with c2: metric_card("Recommended", f'${row["recommended_price"]:.2f}', f'{row["price_change_pct"]:.2f}% price move')
with c3: metric_card("Predicted Gain", f'{row["predicted_revenue_gain_pct"]:.2f}%', "Revenue scenario vs current")
with c4: metric_card("Support", f'{int(row["recommended_price_support_weeks"])} wks', str(row["recommendation_reliability"]) + " reliability")

section_header("SCENARIO COMPARISON","Current vs recommended model output.","The recommendation is restricted to prices historically observed for the same SKU-store in the recent support window.")
fig = go.Figure()
fig.add_bar(name="Predicted Units", x=["Current","Recommended"], y=[row["current_predicted_units"], row["recommended_predicted_units"]], marker_color=["#B7C0D5","#12B5CB"], yaxis="y")
fig.add_scatter(name="Predicted Revenue", x=["Current","Recommended"], y=[row["current_predicted_revenue"], row["recommended_predicted_revenue"]],
                mode="lines+markers", marker=dict(size=13,color="#6C5CE7"), line=dict(width=4,color="#6C5CE7"), yaxis="y2")
fig.update_layout(height=470, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.55)",
                  yaxis=dict(title="Predicted units"), yaxis2=dict(title="Predicted revenue", overlaying="y", side="right"),
                  legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, use_container_width=True)

if abs(float(row["recommended_price"]) - float(row["current_price"])) < 1e-9:
    st.success("Recommendation: HOLD. The current price is already the highest predicted-revenue supported scenario.")
else:
    st.success(f'Recommendation: move from ${row["current_price"]:.2f} to ${row["recommended_price"]:.2f}. Model-predicted revenue gain: {row["predicted_revenue_gain_pct"]:.2f}%.')

st.caption("PriceGraph Edge reports model-based scenario comparisons. It does not claim causal price elasticity or guaranteed lift.")
