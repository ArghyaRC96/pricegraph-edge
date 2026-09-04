# PriceGraph Edge

PriceGraph Edge is a Data Science-first retail pricing decision-support system built on the Walmart M5 dataset.

It combines:

- Poisson XGBoost demand forecasting
- historically supported price simulation
- portfolio-level pricing recommendations
- recommendation reliability guardrails
- directed cross-product PriceGraph analysis
- robust cross-price ripple modelling
- interactive Streamlit decision support
- Gemini-powered business explanations

Gemini is an explanation layer. It does not calculate prices or replace the Data Science pipeline.

## Live Application

Streamlit Community Cloud

Live URL: https://pricegraph-edge.streamlit.app/

## Core Product Question

PriceGraph Edge answers:

> What happens if I change the price of this product in this store?

A user can:

1. Select a department.
2. Select a product.
3. Select a store.
4. Review the current price.
5. Review the model-supported recommendation.
6. Enter a custom price using a slider or manual input.
7. Run live XGBoost inference.
8. Inspect predicted demand.
9. Inspect predicted revenue.
10. Inspect scenario stability and historical support.
11. Inspect related-product ripple effects.
12. Ask Gemini to explain the evidence.

## Application Pages

### Home

Provides:

- project overview
- model performance
- portfolio statistics
- system architecture

### Pricing Command Center

Provides portfolio-level pricing intelligence including:

- HOLD / INCREASE / DECREASE decisions
- reliability filtering
- predicted revenue-change analysis
- top pricing opportunities
- department filtering
- store filtering
- recommendation review cases

### Product Explorer

Provides product-level comparison across stores including:

- current price
- model-supported price
- price change
- predicted revenue change
- reliability
- store-level comparison

### Price Simulator

The main interactive pricing sandbox.

Users can:

- select department, product, and store
- use a price slider
- manually enter a price
- explore supported and extended scenarios
- run live Poisson XGBoost inference
- compare current and scenario demand
- compare current and scenario revenue
- inspect scenario stability
- inspect related-product demand ripple effects

### PriceGraph

Displays directed cross-product pricing relationships.

Relationship types:

- SUBSTITUTION_LIKE
- COMPLEMENT_LIKE

Evidence tiers:

- STRONG
- MODERATE
- SUPPORTED

PriceGraph relationships are historical associations and are not causal claims.

### AI Pricing Analyst

Gemini converts structured model evidence into business-language explanations.

Gemini does not:

- calculate the recommended price
- retrain XGBoost
- replace the pricing engine
- fabricate numerical results
- claim causal effects

## Dataset

Source:

Walmart M5 Forecasting - Accuracy

Main source files:

- calendar.csv
- sell_prices.csv
- sales_train_evaluation.csv

Original dataset characteristics:

- 3,049 unique products
- 10 stores
- 3 states
- 1,941 daily sales columns

The final pricing portfolio focuses on the FOODS category.

Final portfolio:

- FOODS_1: 20 products
- FOODS_2: 30 products
- FOODS_3: 50 products
- Total: 100 products

Possible SKU-store combinations:

1,000

Final eligible modelling contexts:

999

Excluded combination:

FOODS_2_021 / CA_2

Reason:

Insufficient historical data for the required 52-week lag features.

## Product Selection

Products were ranked using pricing-suitability signals including:

- total units sold
- active sales ratio
- number of unique observed prices
- number of price changes
- historical week coverage
- store coverage

This produced a pricing-focused 100-product portfolio.

## Demand Model

Final model:

Poisson XGBoost

Target:

Weekly units sold

Final feature count:

33

Feature groups include:

- item identity
- department
- store
- state
- selling price
- previous-price movement
- recent normal price
- historical mean price
- lagged demand
- rolling demand
- expanding historical demand
- normalized lag ratios
- normalized rolling ratios
- SNAP activity
- event indicators
- month
- day of month
- week of year

Historical features were constructed using prior observations only.

## Model Experiments

The modelling process evaluated:

- Random Forest
- standard XGBoost
- raw target
- log-transformed target
- Poisson XGBoost
- feature pruning
- macroeconomic variables
- alternative seasonality features
- zero-sales history features

Macroeconomic features did not consistently improve validation performance and were excluded.

Zero-sales history features were also tested and excluded.

Week-of-year improved temporal validation and was retained.

## Final Champion Configuration

Key parameters:

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

The final model was evaluated once on an untouched 52-week test period.

| Metric | Poisson XGBoost | Previous-Week Baseline |
| --- | ---: | ---: |
| MAE | 9.7836 | 10.7932 |
| RMSE | 21.9515 | 23.9208 |
| WAPE | 31.3802% | 34.6182% |
| R2 | 0.8454 | 0.8165 |

The test set was not used for further model tuning.

## Safe Price Simulation

The pricing engine does not treat every historical price as valid.

A supported candidate price must:

- belong to the same SKU-store
- occur within the trailing 52-week window
- have at least 4 weeks of historical support

The current price is always retained.

For every candidate price:

1. Price-dependent features are recalculated.
2. The trained XGBoost model predicts weekly demand.
3. Predicted revenue is calculated as price multiplied by predicted units.
4. Supported scenarios are compared.
5. The highest predicted-revenue supported scenario becomes the model-supported recommendation.

The system does not call this a causal optimum.

## User-Controlled Simulation

The deployed application also lets the user choose a price.

Scenario categories:

- SUPPORTED
- EXTENDED
- OUTSIDE EVIDENCE

SUPPORTED:

The exact price has recent historical support for the selected SKU-store.

EXTENDED:

The exact price was not recently supported, but the price movement remains inside an empirically derived model range.

OUTSIDE EVIDENCE:

The price movement exceeds the evidence boundary and quantitative prediction is withheld.

## Predicted Revenue Terminology

The system distinguishes between:

- Current Predicted Revenue
- Predicted Revenue at Recommended Price
- Predicted Revenue at User Price
- Predicted Revenue Change
- Predicted Revenue Change %

Revenue is predicted after demand is estimated.

There is no concept of "recommended revenue".

The price may be recommended. Revenue is predicted under that price.

## Production Stability Guardrails

A small group of recommendation scenarios produced extreme predicted revenue-change percentages.

Diagnosis:

The percentage arithmetic was mathematically correct, but sharp tree-model response changes combined with small baseline predictions produced commercially misleading percentage values.

Production handling:

- preserve the raw model output for audit
- calculate scenario stability
- classify unstable cases as REVIEW
- withhold misleading percentage-change display
- continue showing absolute predicted demand
- continue showing absolute predicted revenue
- do not cosmetically cap the raw model value

The current production policy uses:

- revenue-change threshold
- upper demand-multiple threshold
- lower demand-multiple threshold

## PriceGraph

PriceGraph discovers directed cross-product historical relationships within the same department.

Relationship direction:

Source Product Price -> Target Product Demand

The analysis includes:

- recent demand normalization
- department-store-week adjustment
- store-level residual demand
- observed source price-change events
- exclusion of target own-price-change weeks
- robust log-demand transformation
- empirical source-price trimming
- event-count requirements
- direction-consistency checks

## Full PriceGraph Screening

Same-department directed relationships tested:

3,700

Supported relationships:

828

Relationship types:

- SUBSTITUTION_LIKE: 450
- COMPLEMENT_LIKE: 378

Evidence tiers:

- STRONG: 129
- MODERATE: 197
- SUPPORTED: 502

Priority graph:

326 STRONG or MODERATE edges

Connected products:

90

Average total connections per product:

6.52

## Product Neighborhood Layer

Each priority edge is represented from both product perspectives.

Priority edges:

326

Neighborhood rows:

652

This allows Streamlit to show product-centric incoming and outgoing relationships rather than one unreadable global network.

## Cross-Price Ripple Models

Priority PriceGraph edges evaluated:

326

Directionally consistent models:

325

Method:

Huber robust regression

Relationship:

Source Product Price -> Target Product Demand

Production safeguards include:

- robust regression
- empirical elasticity winsorization
- edge-specific historical price-movement support
- quantitative ripple output only within evidence range
- direction-only output outside edge-level support

Ripple results are historical associations.

They are not causal elasticity guarantees.

## Ripple UX

When the user selects the same price as the current price:

- price movement equals zero
- related-product demand impact equals zero

The application therefore does not show an empty ripple chart.

Instead it asks the user to move the slider or enter a different price.

For non-zero supported movements:

- positive ripple values indicate estimated demand uplift
- negative ripple values indicate estimated demand pressure

## Gemini AI Analyst

Gemini receives structured evidence from the Data Science system.

Examples include:

- product
- store
- current price
- model-supported price
- predicted demand
- predicted revenue
- predicted revenue change
- scenario stability
- recommendation reliability
- PriceGraph relationships

Gemini explains these outputs in business language.

Numerical decisions remain controlled by the modelling pipeline.

## Production Architecture

    Walmart M5 Data
            |
            v
    Feature Engineering
            |
            v
      Poisson XGBoost
            |
       +----+-------------------+
       |                        |
       v                        v
    Price Simulation       PriceGraph Analysis
       |                        |
       v                        v
    Own-SKU Demand         Related-SKU Signals
       |                        |
       v                        v
    Revenue Scenario       Ripple Models
       |                        |
       +-----------+------------+
                   |
                   v
             Streamlit App
                   |
                   v
             Gemini Analyst

## Repository Structure

    pricegraph-edge/
    |
    |-- data/
    |   |-- raw/
    |   `-- processed/
    |
    |-- models/
    |   |-- pricegraph_xgb_poisson.json
    |   |-- pricegraph_preprocessor.joblib
    |   `-- pricegraph_model_metadata.json
    |
    |-- notebooks/
    |   |-- 01_pricegraph_analysis.ipynb
    |   `-- 02_pricegraph_final_pipeline.ipynb
    |
    |-- streamlit/
    |   |-- Home.py
    |   |-- pages/
    |   `-- utils/
    |
    |-- docs/
    |   |-- project_state.md
    |   `-- build_log.md
    |
    |-- requirements.txt
    |-- .gitignore
    `-- README.md

## Notebooks

### 01_pricegraph_analysis.ipynb

Research notebook containing:

- exploratory data analysis
- product selection
- model experiments
- temporal validation
- feature experiments
- demand regime analysis
- macroeconomic experiments
- diagnostics

### 02_pricegraph_final_pipeline.ipynb

Clean final pipeline containing:

- data construction
- leakage-safe feature engineering
- locked temporal split
- champion model training
- final evaluation
- model persistence
- safe pricing engine
- portfolio recommendations
- recommendation reliability
- PriceGraph construction
- ripple modelling
- deployment artifact generation

## Production Artifacts

Main data artifacts:

- simulation_context.csv
- supported_price_candidates.csv
- scenario_policy.json
- portfolio_price_recommendations_enriched.csv
- pricegraph_nodes.csv
- pricegraph_priority_edges.csv
- pricegraph_neighborhoods.csv
- cross_price_ripple_models_production.csv

Main model artifacts:

- pricegraph_xgb_poisson.json
- pricegraph_preprocessor.joblib
- pricegraph_model_metadata.json

## Running Locally

Create virtual environment:

    python -m venv .venv

Activate:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

Run Streamlit:

    streamlit run .\streamlit\Home.py

## Deployment

Platform:

Streamlit Community Cloud

Repository:

ArghyaRC96/pricegraph-edge

Branch:

main

Application entry point:

streamlit/Home.py

Deployment Python:

3.13

Gemini API credentials are stored through Streamlit Secrets.

The API key is never committed to GitHub.

## Limitations

PriceGraph Edge is a portfolio Data Science system rather than a production retail pricing platform.

Important limitations:

- Walmart M5 does not provide inventory availability.
- Zero sales cannot automatically be interpreted as stockouts.
- XGBoost pricing responses are observational.
- PriceGraph relationships are associational.
- Ripple models do not establish causal elasticity.
- Predictions outside historical evidence are restricted.
- Revenue excludes product cost and margin.
- Inventory constraints are not modelled.
- Operational constraints are not modelled.
- M5 item names are anonymized.
- Department semantics are not inferred beyond supplied dataset labels.

## Tech Stack

- Python
- Pandas
- NumPy
- scikit-learn
- XGBoost
- Plotly
- NetworkX
- Streamlit
- Google Gemini API
- Git
- GitHub

## Project Positioning

PriceGraph Edge demonstrates an end-to-end Data Science workflow covering:

- problem framing
- retail data preparation
- leakage-safe feature engineering
- temporal validation
- model comparison
- model diagnostics
- pricing simulation
- production guardrails
- graph analytics
- robust cross-price modelling
- interactive deployment
- responsible Generative AI integration

Core principle:

> The model provides evidence. The user makes the pricing decision.