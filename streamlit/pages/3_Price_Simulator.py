import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.ui import (
    inject_theme,
    metric_card,
    section_header
)

from utils.data_loader import (
    load_app_data,
    load_model_assets
)


st.set_page_config(
    page_title="Price Simulator | PriceGraph Edge",
    layout="wide"
)


inject_theme()


data = load_app_data()

context = data["simulation_context"]
supported_prices = data["supported_prices"]
recommendations = data["recommendations"]
ripple_models = data["ripple_models"]
policy = data["scenario_policy"]


st.title(
    "What if I set this price?"
)

st.caption(
    "Choose a product and store, enter your own price, "
    "and run the trained Poisson XGBoost demand model live. "
    "PriceGraph then estimates supported related-product ripple effects."
)


if context is None:

    st.error(
        "simulation_context.csv is missing."
    )

    st.stop()


if policy is None:

    st.error(
        "scenario_policy.json is missing."
    )

    st.stop()


# ============================================================
# SELECT PRODUCT
# ============================================================

select_1, select_2, select_3 = (
    st.columns(3)
)


with select_1:

    departments = sorted(
        context[
            "dept_id"
        ]
        .dropna()
        .unique()
    )

    selected_dept = st.selectbox(
        "Department",
        departments
    )


dept_context = (
    context[
        context[
            "dept_id"
        ] == selected_dept
    ]
)


with select_2:

    products = sorted(
        dept_context[
            "item_id"
        ]
        .unique()
    )

    selected_item = st.selectbox(
        "Product",
        products
    )


product_context = (
    dept_context[
        dept_context[
            "item_id"
        ] == selected_item
    ]
)


with select_3:

    stores = sorted(
        product_context[
            "store_id"
        ]
        .unique()
    )

    selected_store = st.selectbox(
        "Store",
        stores
    )


scenario_match = (
    product_context[
        product_context[
            "store_id"
        ] == selected_store
    ]
)


if scenario_match.empty:

    st.error(
        "No valid simulation context exists "
        "for this product-store combination."
    )

    st.stop()


scenario_row = (
    scenario_match
    .iloc[0]
    .copy()
)


current_price = float(
    scenario_row[
        "sell_price"
    ]
)


# ============================================================
# MODEL RECOMMENDATION
# ============================================================

recommendation_row = None


if recommendations is not None:

    recommendation_match = (
        recommendations[
            (
                recommendations[
                    "item_id"
                ] == selected_item
            )
            &
            (
                recommendations[
                    "store_id"
                ] == selected_store
            )
        ]
    )


    if not recommendation_match.empty:

        recommendation_row = (
            recommendation_match
            .iloc[0]
        )


if recommendation_row is not None:

    recommended_price = float(
        recommendation_row[
            "recommended_price"
        ]
    )

    reliability = str(
        recommendation_row[
            "recommendation_reliability"
        ]
    )

else:

    recommended_price = (
        current_price
    )

    reliability = "N/A"


# ============================================================
# PRICE RANGE POLICY
# ============================================================

lower_pct = float(
    policy[
        "extended_price_change_lower_pct"
    ]
)

upper_pct = float(
    policy[
        "extended_price_change_upper_pct"
    ]
)


extended_min = max(
    0.01,
    current_price
    *
    (
        1
        +
        lower_pct / 100
    )
)


extended_max = (
    current_price
    *
    (
        1
        +
        upper_pct / 100
    )
)


# ============================================================
# SUPPORTED PRICES
# ============================================================

if supported_prices is not None:

    supported_pair = (
        supported_prices[
            (
                supported_prices[
                    "item_id"
                ] == selected_item
            )
            &
            (
                supported_prices[
                    "store_id"
                ] == selected_store
            )
        ]
        .copy()
    )

else:

    supported_pair = (
        pd.DataFrame()
    )


if not supported_pair.empty:

    candidate_values = (
        supported_pair[
            "candidate_price"
        ]
        .astype(float)
        .tolist()
    )

else:

    candidate_values = []


# ============================================================
# PRICE INPUT
# ============================================================

section_header(
    "SCENARIO INPUT",
    "Set your price.",
    "Use the slider or enter an exact price manually."
)


input_left, input_right = (
    st.columns(
        [1.6, 1]
    )
)


with input_left:

    slider_price = st.slider(
        "Extended scenario range",
        min_value=float(
            round(
                extended_min,
                2
            )
        ),
        max_value=float(
            round(
                extended_max,
                2
            )
        ),
        value=float(
            round(
                current_price,
                2
            )
        ),
        step=0.01
    )


with input_right:

    input_mode = st.radio(
        "Price input mode",
        [
            "Slider",
            "Manual"
        ],
        horizontal=True
    )


    manual_price = st.number_input(
        "Manual price",
        min_value=0.01,
        value=float(
            round(
                current_price,
                2
            )
        ),
        step=0.01
    )


if input_mode == "Slider":

    proposed_price = float(
        slider_price
    )

else:

    proposed_price = float(
        manual_price
    )


price_change_pct = (
    (
        proposed_price
        -
        current_price
    )
    /
    current_price
    *
    100
)


# ============================================================
# EVIDENCE STATUS
# ============================================================

is_supported = any(
    np.isclose(
        proposed_price,
        candidate,
        atol=0.005
    )
    for candidate
    in candidate_values
)


inside_extended_range = (
    lower_pct
    <= price_change_pct
    <= upper_pct
)


if is_supported:

    evidence_status = (
        "SUPPORTED"
    )

    evidence_message = (
        "This exact price has recent historical support "
        "for this SKU-store."
    )

elif inside_extended_range:

    evidence_status = (
        "EXTENDED"
    )

    evidence_message = (
        "This exact price was not a supported recent candidate, "
        "but the price movement remains inside the empirical model range."
    )

else:

    evidence_status = (
        "OUTSIDE EVIDENCE"
    )

    evidence_message = (
        "This scenario exceeds the empirical price-movement range. "
        "Quantitative prediction is disabled."
    )


card_1, card_2, card_3 = (
    st.columns(3)
)


with card_1:

    metric_card(
        "CURRENT PRICE",
        f"${current_price:.2f}",
        "Latest model context"
    )


with card_2:

    metric_card(
        "MODEL RECOMMENDATION",
        f"${recommended_price:.2f}",
        f"Reliability: {reliability}"
    )


with card_3:

    metric_card(
        "YOUR SCENARIO",
        f"${proposed_price:.2f}",
        f"{price_change_pct:+.2f}% vs current"
    )


if evidence_status == "SUPPORTED":

    st.success(
        "SUPPORTED: "
        + evidence_message
    )

elif evidence_status == "EXTENDED":

    st.info(
        "EXTENDED: "
        + evidence_message
    )

else:

    st.warning(
        "OUTSIDE EVIDENCE: "
        + evidence_message
    )


# ============================================================
# STOP IF OUTSIDE EVIDENCE
# ============================================================

if not inside_extended_range:

    section_header(
        "MODEL OUTPUT",
        "Prediction withheld.",
        "Move the scenario price inside the empirical evidence range."
    )

    st.stop()


# ============================================================
# LOAD REAL MODEL
# ============================================================

try:

    model, preprocessor, metadata = (
        load_model_assets()
    )

except Exception as error:

    st.error(
        "Unable to load production model assets."
    )

    st.code(
        str(error)
    )

    st.stop()


features = metadata[
    "features"
]


# ============================================================
# SCENARIO FEATURE ENGINEERING
# ============================================================

def safe_float(
    value,
    fallback
):

    try:

        value = float(
            value
        )

        if np.isfinite(
            value
        ):

            return value

    except Exception:

        pass

    return float(
        fallback
    )


def build_scenario(
    base_row,
    price
):

    row = (
        base_row
        .copy()
    )


    row[
        "sell_price"
    ] = price


    previous_price = safe_float(
        row[
            "previous_price"
        ],
        current_price
    )


    normal_price = safe_float(
        row[
            "normal_price_13wk"
        ],
        current_price
    )


    hist_mean_price = safe_float(
        row[
            "hist_mean_price"
        ],
        current_price
    )


    if previous_price <= 0:

        previous_price = (
            current_price
        )


    if normal_price <= 0:

        normal_price = (
            current_price
        )


    if hist_mean_price <= 0:

        hist_mean_price = (
            current_price
        )


    row[
        "price_change_pct"
    ] = (
        (
            price
            -
            previous_price
        )
        /
        previous_price
        *
        100
    )


    row[
        "price_vs_normal_pct"
    ] = (
        (
            price
            -
            normal_price
        )
        /
        normal_price
        *
        100
    )


    row[
        "price_vs_hist_mean_pct"
    ] = (
        (
            price
            -
            hist_mean_price
        )
        /
        hist_mean_price
        *
        100
    )


    row[
        "price_down_flag"
    ] = int(
        price
        <
        previous_price
    )


    row[
        "price_up_flag"
    ] = int(
        price
        >
        previous_price
    )


    return row


current_scenario = (
    build_scenario(
        scenario_row,
        current_price
    )
)


proposed_scenario = (
    build_scenario(
        scenario_row,
        proposed_price
    )
)


scenario_frame = (
    pd.DataFrame(
        [
            current_scenario,
            proposed_scenario
        ]
    )
)


for column in [
    "item_id",
    "dept_id",
    "store_id",
    "state_id"
]:

    scenario_frame[
        column
    ] = (
        scenario_frame[
            column
        ]
        .astype(str)
    )


# ============================================================
# LIVE XGBOOST PREDICTION
# ============================================================

try:

    transformed = (
        preprocessor.transform(
            scenario_frame[
                features
            ]
        )
    )


    predictions = (
        model.predict(
            transformed
        )
    )


except Exception as error:

    st.error(
        "Live XGBoost inference failed."
    )

    st.code(
        str(error)
    )

    st.stop()


predictions = np.clip(
    predictions,
    0,
    None
)


current_units = float(
    predictions[0]
)


scenario_units = float(
    predictions[1]
)


current_revenue = (
    current_price
    *
    current_units
)


scenario_revenue = (
    proposed_price
    *
    scenario_units
)


if current_units > 0:

    demand_change_pct = (
        (
            scenario_units
            -
            current_units
        )
        /
        current_units
        *
        100
    )

else:

    demand_change_pct = 0.0


if current_revenue > 0:

    revenue_change_pct = (
        (
            scenario_revenue
            -
            current_revenue
        )
        /
        current_revenue
        *
        100
    )

else:

    revenue_change_pct = 0.0


# ============================================================
# LIVE SCENARIO STABILITY GUARDRAIL
# ============================================================

max_revenue_change_pct = float(
    policy.get(
        "max_display_revenue_change_pct",
        100.0
    )
)

max_demand_multiple = float(
    policy.get(
        "max_display_demand_multiple",
        3.0
    )
)

min_demand_multiple = float(
    policy.get(
        "min_display_demand_multiple",
        1.0 / 3.0
    )
)

demand_multiple = (
    scenario_units
    /
    max(
        current_units,
        1e-9
    )
)

unstable_live_scenario = (
    revenue_change_pct
    > max_revenue_change_pct
    or
    demand_multiple
    > max_demand_multiple
    or
    demand_multiple
    < min_demand_multiple
)

if unstable_live_scenario:
    revenue_change_display = "WITHHELD"
else:
    revenue_change_display = (
        f"{revenue_change_pct:+.2f}% vs current"
    )


# ============================================================
# LIVE OUTPUT
# ============================================================

section_header(
    "LIVE MODEL OUTPUT",
    "Scenario impact.",
    "The saved Poisson XGBoost model is running live in the Streamlit backend."
)


output_1, output_2, output_3, output_4 = (
    st.columns(4)
)


with output_1:

    metric_card(
        "PREDICTED DEMAND",
        f"{scenario_units:,.1f}",
        f"{demand_change_pct:+.2f}% vs current"
    )


with output_2:

    metric_card(
        "PREDICTED REVENUE",
        f"${scenario_revenue:,.2f}",
        f"{revenue_change_pct:+.2f}% vs current"
    )


with output_3:

    metric_card(
        "CURRENT DEMAND",
        f"{current_units:,.1f}",
        "Model baseline"
    )


with output_4:

    metric_card(
        "CURRENT REVENUE",
        f"${current_revenue:,.2f}",
        "Model baseline"
    )


if unstable_live_scenario:

    st.warning(
        "Predicted revenue change percentage withheld. "
        "The model response changes too sharply relative "
        "to the current baseline. Review the absolute "
        "predicted demand and revenue values instead."
    )


# ============================================================
# CURRENT VS SCENARIO CHART
# ============================================================

comparison_fig = go.Figure()


comparison_fig.add_trace(
    go.Bar(
        x=[
            "Current",
            "Your Scenario"
        ],
        y=[
            current_revenue,
            scenario_revenue
        ],
        text=[
            f"${current_revenue:,.2f}",
            f"${scenario_revenue:,.2f}"
        ],
        textposition="outside",
        marker_color=[
            "#B8C4F2",
            "#6E63E8"
        ]
    )
)


comparison_fig.update_layout(
    title="Predicted Weekly Revenue",
    height=380,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    yaxis_title="Revenue"
)


st.plotly_chart(
    comparison_fig,
    use_container_width=True
)


# ============================================================
# PRICEGRAPH RIPPLE
# ============================================================

section_header(
    "PRICEGRAPH RIPPLE",
    "Related-product impact.",
    "Quantitative ripple estimates are shown only when "
    "the selected price movement is supported by edge-level history."
)


if ripple_models is None:

    st.info(
        "Ripple-model artifact is unavailable."
    )

    st.stop()


outgoing = (
    ripple_models[
        ripple_models[
            "source_item"
        ] == selected_item
    ]
    .copy()
)


if outgoing.empty:

    st.info(
        "No quantitative outgoing PriceGraph relationships "
        "are available for this product."
    )

    st.stop()


log_move = np.log(
    proposed_price
    /
    current_price
)


ripple_rows = []


for _, edge in (
    outgoing.iterrows()
):

    lower = float(
        edge[
            "supported_log_move_lower"
        ]
    )

    upper = float(
        edge[
            "supported_log_move_upper"
        ]
    )


    within_support = (
        lower
        <= log_move
        <= upper
    )


    relationship = str(
        edge[
            "relationship_type"
        ]
    )


    if within_support:

        elasticity = float(
            edge[
                "production_elasticity"
            ]
        )


        impact_pct = (
            np.expm1(
                elasticity
                *
                log_move
            )
            *
            100
        )


        status = (
            "QUANTIFIED"
        )

    else:

        impact_pct = np.nan

        status = (
            "DIRECTION ONLY"
        )


    if relationship == "SUBSTITUTION_LIKE":

        if proposed_price > current_price:

            pressure = "UP"

        elif proposed_price < current_price:

            pressure = "DOWN"

        else:

            pressure = "NEUTRAL"

    else:

        if proposed_price > current_price:

            pressure = "DOWN"

        elif proposed_price < current_price:

            pressure = "UP"

        else:

            pressure = "NEUTRAL"


    ripple_rows.append(
        {
            "Related Product":
                edge[
                    "target_item"
                ],

            "Relationship":
                relationship,

            "Evidence":
                edge[
                    "edge_strength"
                ],

            "Estimated Demand Impact %":
                impact_pct,

            "Expected Pressure":
                pressure,

            "Status":
                status,

            "Historical Events":
                int(
                    edge[
                        "price_change_events"
                    ]
                )
        }
    )


ripple_df = pd.DataFrame(
    ripple_rows
)


if np.isclose(
    proposed_price,
    current_price,
    atol=0.005
):

    st.info(
        "Your scenario price is the same as the current price. "
        "Move the slider or enter a different manual price "
        "to see related-product ripple effects."
    )

else:

    quantified = (
        ripple_df[
            ripple_df[
                "Status"
            ] == "QUANTIFIED"
        ]
        .copy()
    )


    if quantified.empty:

        st.info(
            "No related-product ripple can be quantified "
            "for this particular price movement. "
            "The relationship table below still shows "
            "directional PriceGraph evidence."
        )

    else:

        quantified[
            "Absolute Impact"
        ] = (
            quantified[
                "Estimated Demand Impact %"
            ]
            .abs()
        )


        quantified = (
            quantified
            .sort_values(
                "Absolute Impact",
                ascending=False
            )
            .head(10)
        )


        chart_data = (
            quantified
            .sort_values(
                "Estimated Demand Impact %",
                ascending=True
            )
        )


        bar_colors = [
            "#11888F"
            if value > 0
            else "#C94F86"
            for value in chart_data[
                "Estimated Demand Impact %"
            ]
        ]


        max_abs_impact = max(
            float(
                chart_data[
                    "Estimated Demand Impact %"
                ]
                .abs()
                .max()
            ),
            0.10
        )


        ripple_fig = go.Figure()


        ripple_fig.add_trace(
            go.Bar(
                x=
                    chart_data[
                        "Estimated Demand Impact %"
                    ],

                y=
                    chart_data[
                        "Related Product"
                    ],

                orientation="h",

                text=
                    chart_data[
                        "Estimated Demand Impact %"
                    ]
                    .map(
                        lambda value:
                        f"{value:+.2f}%"
                    ),

                textposition="outside",

                marker_color=
                    bar_colors
            )
        )


        ripple_fig.update_layout(
            title=
                "Estimated Related-Product Demand Ripple",

            height=max(
                340,
                len(chart_data)
                * 58
            ),

            margin=dict(
                l=20,
                r=70,
                t=60,
                b=30
            ),

            plot_bgcolor=
                "rgba(0,0,0,0)",

            paper_bgcolor=
                "rgba(0,0,0,0)",

            xaxis_title=
                "Estimated demand change (%)",

            yaxis_title="",

            xaxis=dict(
                range=[
                    -max_abs_impact * 1.30,
                    max_abs_impact * 1.30
                ],

                zeroline=True,

                zerolinewidth=2,

                zerolinecolor=
                    "#7A8294",

                gridcolor=
                    "rgba(100,110,130,0.10)"
            )
        )


        st.plotly_chart(
            ripple_fig,
            use_container_width=True
        )


        st.caption(
            "Positive values indicate estimated demand uplift. "
            "Negative values indicate estimated demand pressure."
        )


ripple_display = (
    ripple_df
    .copy()
)


ripple_display[
    "Estimated Demand Impact %"
] = (
    ripple_display[
        "Estimated Demand Impact %"
    ]
    .round(2)
)


st.dataframe(
    ripple_display,
    use_container_width=True,
    hide_index=True
)


st.caption(
    "All demand, revenue and cross-product ripple estimates "
    "are model-based historical associations and are not causal guarantees."
)