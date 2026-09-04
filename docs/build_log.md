# PriceGraph Edge - Build Log

## 1. Project Definition

Defined PriceGraph Edge as a Data Science-heavy retail pricing portfolio project.

Final capability targets:

- demand forecasting
- pricing scenario simulation
- portfolio recommendation engine
- recommendation guardrails
- related-product analysis
- PriceGraph network
- Streamlit deployment
- Gemini explanation layer

Decision:

Gemini would explain Data Science results rather than act as the pricing engine.

## 2. Repository and Dataset

Created:

- local Git repository
- public GitHub repository

Repository:

ArghyaRC96/pricegraph-edge

Loaded Walmart M5 data:

- calendar.csv
- sell_prices.csv
- sales_train_evaluation.csv

## 3. Product Selection

Created pricing suitability metrics using:

- total units
- active-sales ratio
- unique prices
- price changes
- week coverage
- store coverage

Final product portfolio:

- FOODS_1: 20
- FOODS_2: 30
- FOODS_3: 50

Total:

100 products

## 4. Daily and Weekly Modelling Data

Converted wide sales data to long format.

Merged:

- calendar
- events
- SNAP
- weekly prices

Created weekly modelling panel.

Revenue defined as:

price multiplied by units sold

Profit was not modelled because product costs were unavailable.

## 5. Leakage-Safe Features

Created:

- previous price
- prior 13-week median price
- historical expanding mean price
- price-change features
- lag 1 demand
- lag 4 demand
- lag 13 demand
- lag 52 demand
- rolling 4-week demand
- rolling 13-week demand
- historical mean demand
- historical median demand
- normalized lag ratios
- normalized rolling ratios
- SNAP features
- event features
- month
- day of month
- week of year

Historical features used prior observations only.

## 6. Model Experiments

Evaluated:

- Random Forest
- XGBoost
- raw target
- log target
- Poisson objective
- feature subsets
- macroeconomic features
- seasonality features
- zero-sales history

Poisson XGBoost selected as champion.

Macroeconomic features were excluded.

Zero-sales history features were excluded.

Week-of-year was retained.

## 7. Temporal Validation

Used expanding time-series validation.

Final untouched test:

last 52 weeks

The test set remained untouched until the champion was locked.

## 8. Final Champion

Final test metrics:

- MAE: 9.7836
- RMSE: 21.9515
- WAPE: 31.3802%
- R2: 0.8454

Previous-week baseline:

- MAE: 10.7932
- RMSE: 23.9208
- WAPE: 34.6182%
- R2: 0.8165

The champion outperformed the baseline across all aggregate metrics.

## 9. Safe Price Simulation

Initial historical-price simulation exposed temporal confounding.

Older prices sometimes belonged to different demand regimes.

Final simulator rules:

- trailing 52-week price history
- same SKU-store
- minimum 4 weeks support
- current price always retained
- recompute price-dependent features
- no future historical prices

Terminology:

model-supported recommendation

Not:

causal optimum

## 10. Portfolio Recommendations

Expected combinations:

1,000

Final eligible:

999

Excluded:

FOODS_2_021 / CA_2

Reason:

Insufficient history for lag-52 features.

## 11. Recommendation Reliability

Created:

- HIGH
- MEDIUM
- REVIEW

Initial distribution:

- HIGH: 822
- MEDIUM: 97
- REVIEW: 80

Reliability used historical price support and recommendation-risk checks.

## 12. Related-Product Exploration

Raw product-demand correlations showed near-perfect positive relationships.

Conclusion:

Raw correlation was strongly influenced by common temporal demand movement.

Built department-adjusted and residualized demand signals.

Correlation remained candidate evidence only.

## 13. Cross-Price Screening

Constructed directed relationships:

Source Product Price -> Target Product Demand

Screening controlled for:

- target recent demand
- department-store-week movement
- target own-price changes
- source price-change events

## 14. Robust Cross-Price Analysis

Initial percentage demand deviations had extreme tails.

Improvements:

- log-demand deviation
- empirical source-price trimming
- winsorized residual demand
- direction consistency

## 15. Full PriceGraph Screening

Tested every same-department directed relationship.

Total:

3,700

Supported edges:

828

Relationship types:

- substitution-like: 450
- complement-like: 378

## 16. Evidence Tiers

Created:

- STRONG
- MODERATE
- SUPPORTED

Counts:

- STRONG: 129
- MODERATE: 197
- SUPPORTED: 502

Priority graph:

326 edges

## 17. Node and Neighborhood Tables

Built product nodes containing:

- commercial metrics
- pricing summaries
- incoming edges
- outgoing edges
- relationship strength
- strong-edge counts

Connected products:

90

Created product-centric neighborhood rows:

652

## 18. Cross-Price Ripple Models

Built Huber robust regression ripple models.

Models fitted:

326

Directionally consistent:

325

Added:

- elasticity winsorization
- edge-specific historical support
- quantitative output restrictions

## 19. Deployment Artifacts

Created compact production artifacts for Streamlit.

Saved:

- latest simulation context
- supported price candidates
- pricing recommendations
- PriceGraph nodes
- PriceGraph edges
- product neighborhoods
- ripple models
- XGBoost model
- model metadata

## 20. Streamlit Application

Created pages:

- Home
- Pricing Command Center
- Product Explorer
- Price Simulator
- PriceGraph
- AI Pricing Analyst

Created a muted premium UI theme.

## 21. Live User Price Simulation

Implemented:

- department selector
- product selector
- store selector
- slider
- manual price input
- supported-price status
- extended scenario range
- live XGBoost inference
- predicted demand
- predicted revenue
- related-product ripple estimates

## 22. Model Artifact Compatibility

The original serialized scikit-learn preprocessing artifact produced version-compatibility problems between Colab and the local runtime.

Production solution:

Recreate the ColumnTransformer locally using the saved feature schema and deployment context.

The XGBoost JSON model remained portable.

## 23. Production Stability Guardrails

Detected 21 portfolio recommendation cases with extreme percentage revenue changes.

Diagnosis:

The mathematical percentage calculation was correct.

However, sharp tree-model response changes combined with small current predicted baselines produced commercially misleading percentages.

Production solution:

- retain raw values for audit
- flag unstable scenarios
- mark them REVIEW
- withhold misleading percentages
- continue showing absolute demand
- continue showing absolute revenue

No cosmetic clipping of raw model outputs was used.

## 24. Pricing Terminology Cleanup

Clarified that prices may be recommended, but revenue is predicted.

Final terminology includes:

- Current Predicted Revenue
- Predicted Revenue at Recommended Price
- Predicted Revenue at User Price
- Predicted Revenue Change
- Predicted Revenue Change %

Removed ambiguous wording such as:

Recommended Revenue

## 25. Ripple Visualization UX

When proposed price equals current price:

- price movement equals zero
- ripple equals zero

Updated UI:

- no empty ripple chart
- show instruction to change price
- render chart only for non-zero supported movement
- show direction-only relationships when quantitative support is insufficient

## 26. Deployment

Deployment platform:

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

Streamlit Secrets

Production deployment completed.

## Final Status

Data pipeline:

COMPLETE

Model development:

COMPLETE

Temporal evaluation:

COMPLETE

Pricing simulation:

COMPLETE

Portfolio recommendations:

COMPLETE

Recommendation guardrails:

COMPLETE

PriceGraph:

COMPLETE

Ripple models:

COMPLETE

Streamlit:

COMPLETE

Deployment:

COMPLETE

Documentation:

COMPLETE

Remaining:

- add exact live URL
- final documentation commit
- final push
- confirm clean Git status

## 27. Gemini Model Migration

The deployed AI Pricing Analyst returned a provider 404 because gemini-2.5-flash was no longer available to new users.

Updated default model:

gemini-3.6-flash

Only the Gemini model identifier changed.

The pricing model, PriceGraph pipeline, prompts, and numerical decision logic were unchanged.

Python compilation passed and the change was committed and deployed.

## 28. Final Recommendation Guardrail Verification

The deployed AI Pricing Analyst initially continued displaying an extreme recommendation:

FOODS_1_012 / CA_3

Observed stale display:

- Predicted Revenue Change: 825.74%
- Reliability: HIGH

The local production artifact was inspected and confirmed correct:

- predicted_revenue_gain_pct: withheld / NaN
- raw_predicted_revenue_gain_pct: approximately 825.74%
- predicted_demand_multiple: approximately 9.39
- scenario_stability: REVIEW
- recommendation_reliability: REVIEW

This confirmed that the model guardrail and production artifact were correct.

## 29. Streamlit CSV Cache Fix

The deployed application was reading stale cached recommendation data.

Root cause:

load_csv() in streamlit/utils/data_loader.py used st.cache_data.

Because deployment artifacts are compact, the generic CSV cache was removed.

Result:

Streamlit now reloads the current production recommendation artifact after deployment updates.

The change compiled successfully, was committed, pushed, and redeployed.

## 30. Final Production Smoke Test

Final deployed smoke test:

FOODS_1_012 / CA_3

Expected and observed result:

- Predicted Revenue Change: WITHHELD
- Reliability: REVIEW

This confirmed that:

- the guarded production artifact is being loaded,
- stale recommendation caching is resolved,
- unstable model outputs are not presented as trustworthy commercial percentages,
- raw values remain available for audit.

## 31. Final Project Completion

Live application:

https://pricegraph-edge.streamlit.app/

Final stack includes:

- Walmart M5 retail data
- Pandas
- NumPy
- scikit-learn
- Poisson XGBoost
- Plotly
- NetworkX
- Huber regression
- Streamlit
- Gemini 3.6 Flash
- Git
- GitHub

Final project status:

COMPLETE

Final Git expectation:

- branch: main
- origin/main synchronized
- working tree clean
- notebooks committed
- production artifacts committed
- Streamlit application committed
- README committed
- project_state.md committed
- build_log.md committed
