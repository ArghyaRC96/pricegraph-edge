from pathlib import Path
import sys
STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import os
import json
import streamlit as st
from google import genai
from utils.ui import inject_theme, page_header, metric_card, section_header, artifact_missing
from utils.data_loader import load_app_data

st.set_page_config(page_title="AI Pricing Analyst", page_icon="P", layout="wide")
inject_theme()
page_header("EXPLANATION LAYER","AI Pricing Analyst","Gemini explains model outputs and graph evidence. It does not calculate prices, retrain the model, or invent causal claims.")
data = load_app_data()
recs, neigh = data["recommendations"], data["neighborhoods"]

if recs is None:
    artifact_missing(["portfolio_price_recommendations_enriched.csv"])
    st.stop()

item = st.selectbox("Product", sorted(recs["item_id"].unique().tolist()))
stores = sorted(recs.loc[recs["item_id"] == item, "store_id"].unique().tolist())
store = st.selectbox("Store", stores)
row = recs[(recs["item_id"] == item) & (recs["store_id"] == store)].iloc[0]
hood = neigh[neigh["item_id"] == item].head(6).copy() if neigh is not None else None

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Current", f'${row["current_price"]:.2f}', "Current observed price")
with c2: metric_card("Recommended", f'${row["recommended_price"]:.2f}', "Supported model scenario")
with c3: metric_card("Predicted Gain", f'{row["predicted_revenue_gain_pct"]:.2f}%', "Scenario revenue gain")
with c4: metric_card("Reliability", str(row["recommendation_reliability"]), "Transparent guardrail tier")

section_header("ASK THE ANALYST","Turn model output into a concise business explanation.","Try: Why is this price recommended? What are the main risks? How should I interpret the connected products?")
question = st.text_area("Question", value="Explain this recommendation in simple business language and mention the main caution.", height=110)

api_key = os.getenv("GEMINI_API_KEY")
try:
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

facts = {
    "item_id": item,
    "store_id": store,
    "current_price": float(row["current_price"]),
    "recommended_price": float(row["recommended_price"]),
    "price_change_pct": float(row["price_change_pct"]),
    "current_predicted_units": float(row["current_predicted_units"]),
    "recommended_predicted_units": float(row["recommended_predicted_units"]),
    "current_predicted_revenue": float(row["current_predicted_revenue"]),
    "recommended_predicted_revenue": float(row["recommended_predicted_revenue"]),
    "predicted_revenue_gain_pct": float(row["predicted_revenue_gain_pct"]),
    "support_weeks": int(row["recommended_price_support_weeks"]),
    "reliability": str(row["recommendation_reliability"]),
}
relationships = []
if hood is not None:
    for _, r in hood.iterrows():
        relationships.append({
            "neighbor": r["neighbor_item"],
            "direction": r["edge_direction"],
            "type": r["relationship_type"],
            "strength": r["edge_strength"],
            "correlation": round(float(r["cross_price_corr"]),3),
            "events": int(r["price_change_events"])
        })

if not api_key:
    st.info("Add GEMINI_API_KEY to your local .env/environment or Streamlit secrets to activate live explanations.")
else:
    if st.button("Generate analyst brief", type="primary"):
        prompt = f"""
You are the explanation layer for PriceGraph Edge, a retail pricing data-science system.

Rules:
- Explain only the supplied model and graph outputs.
- Do not claim causal elasticity, guaranteed lift, or confirmed substitution/complementarity.
- Call revenue changes model-predicted scenario gains.
- Call graph relationships substitution-like or complement-like.
- Keep the answer concise, practical, and interview-friendly.

Pricing facts:
{json.dumps(facts, indent=2)}

Related-product evidence:
{json.dumps(relationships, indent=2)}

User question:
{question}
"""
        try:
            client = genai.Client(api_key=api_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            with st.spinner("Reading the model evidence..."):
                response = client.models.generate_content(model=model_name, contents=prompt)
            st.markdown("### Analyst brief")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini request failed: {e}")

with st.expander("Evidence supplied to Gemini"):
    st.json({"pricing": facts, "relationships": relationships})
