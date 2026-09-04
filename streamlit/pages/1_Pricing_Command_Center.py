from pathlib import Path
import sys
STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import streamlit as st
import plotly.express as px
from utils.ui import inject_theme, page_header, metric_card, section_header, artifact_missing
from utils.data_loader import load_app_data

st.set_page_config(page_title="Pricing Command Center", page_icon="P", layout="wide")
inject_theme()
page_header("PORTFOLIO INTELLIGENCE","Pricing Command Center","Scan the portfolio, filter decisions, and surface the highest model-predicted pricing opportunities.")
data = load_app_data()
df = data["recommendations"]

if df is None:
    artifact_missing(["portfolio_price_recommendations_enriched.csv"])
    section_header("READY TO ACTIVATE","The page is built, not blank.","As soon as the recommendation artifact is synced, the KPI cards, filters, charts and tables below activate automatically.")
    st.stop()

filters = st.columns(3)
work = df.copy()
with filters[0]:
    dept = st.selectbox("Department", ["All"] + sorted(work["dept_id"].dropna().unique().tolist()))
with filters[1]:
    store = st.selectbox("Store", ["All"] + sorted(work["store_id"].dropna().unique().tolist()))
with filters[2]:
    strengths = st.multiselect("Reliability", sorted(work["recommendation_reliability"].dropna().unique().tolist()), default=sorted(work["recommendation_reliability"].dropna().unique().tolist()))

if dept != "All": work = work[work["dept_id"] == dept]
if store != "All": work = work[work["store_id"] == store]
if strengths: work = work[work["recommendation_reliability"].isin(strengths)]

avg_gain = work["predicted_revenue_gain_pct"].mean() if len(work) else 0
high = int((work["recommendation_reliability"] == "HIGH").sum()) if len(work) else 0
review = int((work["recommendation_reliability"] == "REVIEW").sum()) if len(work) else 0
changes = int((work["price_direction"] != "HOLD").sum()) if len(work) else 0

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Visible Decisions", f"{len(work):,}", "After current filters")
with c2: metric_card("Avg Predicted Gain", f"{avg_gain:.2f}%", "Model-based scenario gain")
with c3: metric_card("HIGH Reliability", f"{high:,}", "Transparent guardrail tier")
with c4: metric_card("Price Changes", f"{changes:,}", f"{review} cases flagged REVIEW")

section_header("PORTFOLIO MIX","What the pricing engine is recommending.","Direction and predicted revenue-gain distributions across the filtered portfolio.")
a,b = st.columns(2)
with a:
    counts = work["price_direction"].value_counts().rename_axis("direction").reset_index(name="count")
    fig = px.pie(counts, names="direction", values="count", hole=.62,
                 color="direction", color_discrete_map={"INCREASE":"#6C5CE7","DECREASE":"#12B5CB","HOLD":"#D7DCE8"})
    fig.update_layout(height=380, margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
with b:
    fig = px.histogram(work, x="predicted_revenue_gain_pct", nbins=35, labels={"predicted_revenue_gain_pct":"Predicted revenue gain (%)"})
    fig.update_traces(marker_color="#6C5CE7")
    fig.update_layout(height=380, margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.55)")
    st.plotly_chart(fig, use_container_width=True)

section_header("TOP OPPORTUNITIES","Highest model-predicted revenue gains.","These are scenario-model outputs, not causal guarantees.")
top = work.nlargest(15, "predicted_revenue_gain_pct").sort_values("predicted_revenue_gain_pct")
fig = px.bar(top, x="predicted_revenue_gain_pct", y="item_id", orientation="h", color="recommendation_reliability",
             color_discrete_map={"HIGH":"#12A67B","MEDIUM":"#6C5CE7","REVIEW":"#FF7A7A"},
             labels={"predicted_revenue_gain_pct":"Predicted revenue gain (%)","item_id":"Product"})
fig.update_layout(height=470, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.55)", legend_title_text="Reliability")
st.plotly_chart(fig, use_container_width=True)

cols = ["item_id","dept_id","store_id","current_price","recommended_price","price_change_pct","predicted_revenue_gain_pct","recommendation_reliability"]
st.dataframe(work[cols].sort_values("predicted_revenue_gain_pct", ascending=False), use_container_width=True, hide_index=True)
