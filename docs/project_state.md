# PriceGraph Edge - Project State

Last updated: September 2026

## Overall Status

Core Data Science pipeline: COMPLETE

Final model: COMPLETE

Safe price simulation: COMPLETE

Portfolio recommendations: COMPLETE

PriceGraph: COMPLETE

Cross-price ripple models: COMPLETE

Streamlit application: COMPLETE

Streamlit Community Cloud deployment: COMPLETE

Documentation: FINALIZING

## Product Definition

PriceGraph Edge is an interactive retail pricing decision-support system built using Walmart M5 data.

Primary user flow:

1. Select department.
2. Select product.
3. Select store.
4. Review current price.
5. Review model-supported price.
6. Set a custom price using slider or manual input.
7. Run live Poisson XGBoost inference.
8. Inspect predicted demand.
9. Inspect predicted revenue.
10. Inspect scenario stability.
11. Inspect related-product ripple effects.
12. Ask Gemini to explain the evidence.

## Final Portfolio

Products:

100

Stores:

10

Departments:

- FOODS_1: 20
- FOODS_2: 30
- FOODS_3: 50

Possible SKU-store combinations:

1,000

Eligible final modelling contexts:

999

Excluded combination:

FOODS_2_021 / CA_2

Reason:

Insufficient history for the required 52-week demand lag.

## Final Model

Model:

Poisson XGBoost

Target:

Weekly units sold

Feature count:

33

Final seasonality feature added:

week_of_year

Year was excluded from the final model.

## Final Locked Parameters

- n_estimators: 625
- learning_rate: 0.035
- max_depth: 6
- min_child_weight: 5
- subsample: 0.9
- colsample_bytree: 0.9
- reg_alpha: 0.1
- reg_lambda: 2
- max_delta_step: 0.7
- objective: count:poisson
- eval_metric: poisson-nloglik
- tree_method: hist
- random_state: 42

## Final Untouched Test Performance

Poisson XGBoost:

- MAE: 9.7836
- RMSE: 21.9515
- WAPE: 31.3802%
- R2: 0.8454

Previous-week baseline:

- MAE: 10.7932
- RMSE: 23.9208
- WAPE: 34.6182%
- R2: 0.8165

The final 52-week test period was not used for further tuning.

## Safe Price Simulator

Supported-price rules:

- trailing 52-week history
- same SKU-store only
- minimum 4 observed weeks
- current price always retained
- no future prices used

User price entry:

- slider
- manual input

Scenario status:

- SUPPORTED
- EXTENDED
- OUTSIDE EVIDENCE

Live model inference runs inside the Streamlit Python backend.

The model is loaded and reused.

It is not retrained on each scenario.

## Production Stability

A small number of recommendations produced extreme percentage revenue changes due to sharp model response changes and small current predicted baselines.

Production handling:

- preserve raw output
- flag unstable scenario
- force REVIEW reliability
- withhold misleading percentage
- continue showing absolute predicted demand
- continue showing absolute predicted revenue

Raw values are not cosmetically clipped.

## PriceGraph

Directed same-department relationships screened:

3,700

Supported:

828

Relationship types:

- SUBSTITUTION_LIKE: 450
- COMPLEMENT_LIKE: 378

Evidence tiers:

- STRONG: 129
- MODERATE: 197
- SUPPORTED: 502

Priority graph:

326 edges

Connected products:

90

Average total connections per product:

6.52

## Ripple Models

Priority edges evaluated:

326

Directionally consistent models:

325

Method:

Huber robust regression

Production safeguards:

- coefficient winsorization
- historical price-movement support
- edge-specific support range
- quantitative output only inside evidence
- direction-only output outside evidence

## Streamlit Pages

- Home
- Pricing Command Center
- Product Explorer
- Price Simulator
- PriceGraph
- AI Pricing Analyst

## Deployment

Platform:

Streamlit Community Cloud

Repository:

ArghyaRC96/pricegraph-edge

Branch:

main

Entry point:

streamlit/Home.py

Python:

3.13

Gemini API key:

Stored through Streamlit Secrets.

Never commit the Gemini API key.

## Local Repository

Location:

C:\Users\User\Desktop\projects\pricegraph-edge

Expected branch:

main

Remote:

https://github.com/ArghyaRC96/pricegraph-edge.git

## Main Production Data Files

- simulation_context.csv
- supported_price_candidates.csv
- scenario_policy.json
- portfolio_price_recommendations_enriched.csv
- pricegraph_nodes.csv
- pricegraph_priority_edges.csv
- pricegraph_neighborhoods.csv
- cross_price_ripple_models_production.csv

## Main Model Files

- pricegraph_xgb_poisson.json
- pricegraph_preprocessor.joblib
- pricegraph_model_metadata.json

## Remaining Administrative Tasks

1. Streamlit URL added to README: https://pricegraph-edge.streamlit.app/
2. Verify Gemini Analyst on deployed application.
3. Final documentation commit.
4. Push to main.
5. Verify clean Git status.
6. Optional final screenshots.

## Interview Positioning

Preferred description:

A Data Science-first retail pricing decision-support system using leakage-safe demand forecasting, supported-price simulation, robust historical cross-product relationship analysis, graph intelligence, and a thin Generative AI explanation layer.

Preferred terminology:

- model-supported price scenario
- predicted revenue at recommended price
- historical cross-price association
- estimated related-product demand impact
- substitution-like
- complement-like

Avoid claiming:

- causal price optimization
- guaranteed elasticity
- reinforcement-learning pricing
- inventory optimization
- profit optimization