# renewable-energy-forecasting

End-to-end machine learning pipeline for forecasting solar irradiance using historical weather data and public renewable energy datasets. The project is designed as a building block for power markets analytics, renewable integration, and dispatch/operations decision-making.

---

# Objectives

- Forecast short-term solar irradiance (e.g., GHI / DNI / DHI or related signals).
- Build a reproducible pipeline from raw data ingestion → feature engineering → model training → evaluation.
- Use model diagnostics (residuals, SHAP) to understand drivers of forecast accuracy.
- Structure the project in a way that can be extended to power markets and grid operations use cases.

---

## Why This Matters (Energy / Power Markets Context)

Accurate renewable forecasts are critical for:

- Day-ahead and intraday power market bidding.
- Scheduling and operating flexible assets (storage, flexible load, data centers, etc.).
- Reducing imbalance costs and improving grid stability as renewable penetration increases.

This project demonstrates how to go from raw weather/irradiance data to a usable forecasting model that could feed into those decision processes.

---

##  Tech Stack

**Languages & Libraries**
- Python (pandas, numpy, scikit-learn, LightGBM)
- PySpark (for scalable feature engineering, if running in Databricks)
- Visualization: matplotlib / seaborn / plotly (as used in notebooks)

**Data & Compute**
- AWS S3 – raw and intermediate data storage
- Databricks – notebooks, ETL, feature engineering, model training
- Snowflake – cleaned / modeled data for downstream analytics

**ML & Explainability**
- Gradient boosting with LightGBM
- Time-series cross-validation
- Residual analysis and error diagnostics
- SHAP for model interpretability

---

## Data Sources

The project uses publicly available renewable and weather datasets, for example:

- Solar irradiance and/or renewable generation data (NREL).
- Weather features from APIs such as Open-Meteo (temperature, cloud cover, wind, etc.).

Raw data is not committed to the repository. Instructions/notebooks describe how to download and place data locally or in cloud storage.

---

# Project Architecture

High-level pipeline:

1. **Data Ingestion**
   - Download or query historical irradiance / weather data.
   - Store raw files in **S3** (or local `/data/raw` during development).

2. **Data Cleaning & Feature Engineering (Databricks / PySpark)**
   - Parse timestamps and align time zones.
   - Handle missing values and outliers.
   - Engineer time-based features (hour, day, month, season, etc.).
   - Join weather features with irradiance / target series.
   - Persist cleaned, feature-ready data to **Snowflake** (or `/data/processed`).

3. **Modeling (Python / LightGBM)**
   - Train/validation split with time-series awareness.
   - Train LightGBM regression models on engineered features.
   - Evaluate using MAE, RMSE and visual diagnostics (forecast vs. actual, residual plots).

4. **Interpretability & Diagnostics (SHAP)**
   - Compute SHAP values to understand which features drive predictions.
   - Analyze how weather and time features contribute to forecast quality.

5. **Extensions (Future Work)**
   - Integrate forecasts into power market / dispatch simulations.
   - Add more advanced models (e.g., neural nets, probabilistic forecasts).
   - Productionize via scheduled jobs or model serving if needed.
