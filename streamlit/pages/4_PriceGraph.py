from pathlib import Path
import sys
STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

import math
import streamlit as st
import plotly.graph_objects as go
from utils.ui import inject_theme, page_header, metric_card, section_header, artifact_missing
from utils.data_loader import load_app_data

st.set_page_config(page_title="PriceGraph", page_icon="P", layout="wide")
inject_theme()
page_header("GRAPH INTELLIGENCE","PriceGraph","Explore directed cross-price relationships. Focus on one product at a time so the network stays interpretable instead of becoming a 326-edge hairball.")
data = load_app_data()
nodes, neigh = data["nodes"], data["neighborhoods"]

if nodes is None or neigh is None:
    missing = []
    if nodes is None: missing.append("pricegraph_nodes.csv")
    if neigh is None: missing.append("pricegraph_neighborhoods.csv")
    artifact_missing(missing)
    st.stop()

connected = nodes[nodes["total_connections"] > 0].copy()
item = st.selectbox("Focus product", sorted(connected["item_id"].tolist()))
max_neighbors = st.slider("Neighbors", 4, 15, 10)

node = nodes[nodes["item_id"] == item].iloc[0]
hood = neigh[neigh["item_id"] == item].sort_values(["strength_rank","absolute_cross_price_corr"], ascending=[True,False]).head(max_neighbors).copy()

c1,c2,c3,c4 = st.columns(4)
with c1: metric_card("Connections", str(int(node["total_connections"])), "Incoming + outgoing priority links")
with c2: metric_card("Strong Links", str(int(node["total_strong_connections"])), "Strong evidence tier")
with c3: metric_card("Outgoing", str(int(node["outgoing_edges"])), "Your price -> neighbor demand")
with c4: metric_card("Incoming", str(int(node["incoming_edges"])), "Neighbor price -> your demand")

section_header("FOCUS NETWORK",f"{item} and its strongest neighbors.","Purple edges are substitution-like; cyan edges are complement-like. Arrow direction preserves the historical source-price -> target-demand relationship.")

n = len(hood)
positions = {item:(0.0,0.0)}
for i, neighbor in enumerate(hood["neighbor_item"]):
    angle = 2 * math.pi * i / max(n,1)
    positions[neighbor] = (math.cos(angle), math.sin(angle))

fig = go.Figure()

for _, r in hood.iterrows():
    neighbor = r["neighbor_item"]
    center = positions[item]
    other = positions[neighbor]
    if r["edge_direction"] == "OUTGOING":
        start, end = center, other
    else:
        start, end = other, center
    color = "#6C5CE7" if r["relationship_type"] == "SUBSTITUTION_LIKE" else "#12B5CB"
    width = 2.0 + 5.0 * float(abs(r["cross_price_corr"]))
    fig.add_trace(go.Scatter(
        x=[start[0], end[0]], y=[start[1], end[1]],
        mode="lines",
        line=dict(color=color, width=width),
        hoverinfo="skip",
        showlegend=False
    ))
    fig.add_annotation(
        x=end[0], y=end[1], ax=start[0], ay=start[1],
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=1.2, arrowcolor=color,
        opacity=.85
    )

neighbor_x, neighbor_y, neighbor_text, neighbor_hover = [], [], [], []
for _, r in hood.iterrows():
    x,y = positions[r["neighbor_item"]]
    neighbor_x.append(x); neighbor_y.append(y); neighbor_text.append(r["neighbor_item"])
    neighbor_hover.append(
        f'{r["neighbor_item"]}<br>{r["relationship_type"]}<br>{r["edge_strength"]}<br>r={r["cross_price_corr"]:.3f}<br>{int(r["price_change_events"])} events'
    )

fig.add_trace(go.Scatter(
    x=neighbor_x, y=neighbor_y, mode="markers+text",
    text=neighbor_text, textposition="top center",
    hovertext=neighbor_hover, hoverinfo="text",
    marker=dict(size=26, color="#FFFFFF", line=dict(width=4,color="#9A8DF0")),
    textfont=dict(size=11,color="#344054"),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode="markers+text",
    text=[item], textposition="bottom center",
    hovertext=[f'{item}<br>{int(node["total_connections"])} total connections'],
    hoverinfo="text",
    marker=dict(size=48,color="#6C5CE7",line=dict(width=7,color="#DDD7FF")),
    textfont=dict(size=13,color="#162033"),
    showlegend=False
))
fig.update_layout(
    height=650, margin=dict(l=20,r=20,t=20,b=20),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.55)",
    xaxis=dict(visible=False, range=[-1.35,1.35]), yaxis=dict(visible=False, range=[-1.35,1.35]),
    hoverlabel=dict(bgcolor="white", font_color="#162033")
)
st.plotly_chart(fig, use_container_width=True)

section_header("RELATIONSHIP EVIDENCE","The graph is backed by historical price-change events.","These labels describe associational evidence strength, not causal confidence.")
cols = ["neighbor_item","edge_direction","relationship_type","edge_strength","cross_price_corr","price_change_events"]
st.dataframe(hood[cols], use_container_width=True, hide_index=True)
