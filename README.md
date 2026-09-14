# 🌬️ Air Quality & CPCB NAQI Analytical Engine & Intelligence Platform

> **Multi-Year Environmental, Chemical, and Meteorological Investigation (2017–2023)**  
> *Engineered in strict accordance with the Central Pollution Control Board (CPCB) National Air Quality Index (NAQI) guidelines of India.*

---

## 📌 Executive Overview

This repository houses an **end-to-end environmental data science platform** that ingests, cleans, calculates, forecasts, visualizes, and reports on ambient air quality across **5 calendar years (2017, 2018, 2021, 2022, and 2023)**, totaling **1,825 daily monitoring records** and **24 environmental parameters**.

### Key Capabilities
- **Automated Data Engineering**: Cleans and consolidates heterogeneous multi-year sensor logs with variable date formats and missing data patterns into a unified staged dataset.
- **Official CPCB NAQI Engine**: Implements piecewise linear interpolation breakpoints across 7 criteria pollutants ($PM_{2.5}, PM_{10}, NO_2, NH_3, SO_2, CO, Ozone$) with minimum validity rules ($\ge 3$ pollutants including at least one particulate parameter).
- **Environmental Diagnostic Ratios**: Fine particle combustion fraction ($PM_{2.5}/PM_{10}$), Volatile Organic Compound fingerprinting ($Toluene/Benzene$ ratio, Total BTX), and ventilation dispersion proxy.
- **Predictive Machine Learning**: Supervised 24-hour ahead AQI forecasting engine achieving **$R^2 = 0.769$** on true out-of-time prospective testing (Year 2023).
- **Directional Source Apportionment**: Wind direction ($WD$) polar pollution rose modeling and empirical emission regime classification.
- **Interactive Web Dashboard**: High-performance dark-mode analytics console built with HTML5, Vanilla CSS, and Plotly.js.
- **Automated Unit Testing Suite**: Verifies breakpoint formulas, edge cases, and CPCB category boundaries.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["Raw Monitoring Logs (data/raw/*.csv)"] --> B["Stage 1: Data Ingestion (pipeline/data_ingestion.py)"]
    B --> C["Staged Dataset (data/processed/air_quality_staged.csv)"]
    C --> D["Stage 2: Preprocessing & Feature Engineering (pipeline/preprocessing.py)"]
    D --> E["Stage 3: CPCB NAQI Engine (pipeline/aqi_engine.py)"]
    E --> F["Cleaned Dataset (data/processed/air_quality_clean.csv)"]
    
    F --> G["Stage 4: Statistical Profiling (reports/component_statistics.csv)"]
    F --> H["Stage 5: Visualization Suite (outputs/plots/01-07)"]
    F --> I["Stage 6: Predictive ML Forecasting (pipeline/forecasting.py -> 08_forecast)"]
    F --> J["Stage 7: Source Apportionment & Wind Roses (pipeline/source_apportionment.py -> 09_roses)"]
    
    F --> K["Export: Dashboard JSON Sync (outputs/data/cleaned.json)"]
    K --> L["Interactive Web UI (web/index.html + app.js)"]
    G & I & J --> M["Scientific Report (reports/air_quality_analysis_report.md)"]
```

---

## 🔬 Monitored Environmental Parameters (24 Components)

| Parameter Group | Monitored Species / Metrics | Description & Standards |
| :--- | :--- | :--- |
| **Criteria Particulates** | $PM_{2.5}$, $PM_{10}$ | Primary AQI drivers (NAAQS: $60\ \mu g/m^3$ & $100\ \mu g/m^3$) |
| **Reactive Nitrogen** | $NO$, $NO_2$, $NO_x$, $NH_3$ | Vehicular combustion & agricultural emissions (NAAQS: $NO_2=80\ \mu g/m^3$, $NH_3=400\ \mu g/m^3$) |
| **Sulfur & Carbon** | $SO_2$, $CO$ | Industrial/coal emissions & incomplete combustion ($SO_2=80\ \mu g/m^3$, $CO=2.0\ mg/m^3$) |
| **Photochemical Oxidants** | $Ozone\ (O_3)$ | Secondary tropospheric smog formed via solar irradiance ($O_3=100\ \mu g/m^3$) |
| **Volatile Aromatics (BTEX)**| $Benzene, Toluene, Xylene, O\text{-}Xylene, Eth\text{-}Benzene, MP\text{-}Xylene$ | Hazardous aromatics, traffic markers, and solvents ($Benzene=5.0\ \mu g/m^3$) |
| **Meteorology & Dynamics** | $AT, RH, WS, WD, RF, TOT\_RF, SR, BP, VWS$ | Ambient Temp, Relative Humidity, Wind Dir, Rain, Solar Rad, Barometric Pressure |

---

## 🚀 Quick Start & Usage

### 1. Environment Setup
Clone or enter the directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Automated Verification Tests
Run the unit testing suite to verify CPCB formulas, breakpoint boundaries, and preprocessing calculations:
```bash
python test.py
```

### 3. Execute the Master Pipeline
Execute the full 7-stage analytical pipeline from raw data to plots, machine learning forecasts, and web JSON:
```bash
python main_pipeline.py
```

### 4. Launch the Interactive Web Dashboard
Serve the interactive Plotly dashboard locally:
```bash
python -m http.server 8000 --directory web
```
Then navigate to `http://localhost:8000` in your web browser.

---

## 📊 Summary of Findings

| Metric | Result | Interpretation |
| :--- | :---: | :--- |
| **Mean Composite AQI** | **221.23 ± 123.17** | Airshed categorized as **Poor** on average |
| **Unhealthy Days (AQI > 100)** | **78.82%** (897 days) | Majority of days exceed acceptable public health limits |
| **Severe Days (AQI > 400)** | **8.52%** (97 days) | Acute hazardous winter episodes requiring emergency GRAP |
| **Primary AQI Drivers** | **$PM_{2.5}$ (51.8%) & $PM_{10}$ (43.5%)** | Particulates account for **95.26%** of all peak episodes |
| **24-hr Forecast $R^2$ Score** | **0.769** (RMSE: 54.98) | High predictive capacity for next-day early warning alerts |
| **Dominant Smog Sector** | **Northwest ($300^\circ-330^\circ$)** | Transboundary transport during post-monsoon stubble fires |

---

## 📂 Repository Structure

```
├── data/
│   ├── raw/                 # Multi-year raw CSVs (2017-2023)
│   └── processed/           # Staged and clean datasets with computed AQI
├── outputs/
│   ├── data/                # Synchronized JSON feed (cleaned.json) for web dashboard
│   └── plots/               # Nine 300-DPI publication-grade figures (01 to 09)
├── pipeline/
│   ├── data_ingestion.py    # Multi-year schema normalization
│   ├── preprocessing.py     # Seasonal flags & diagnostic ratios
│   ├── aqi_engine.py        # CPCB piecewise linear NAQI calculator
│   ├── visualizer.py        # 300-DPI Matplotlib/Seaborn visualizer
│   ├── forecasting.py       # Supervised 24-hr AQI predictive ML models
│   └── source_apportionment.py # Directional wind rose & chemical fingerprinting
├── reports/
│   ├── air_quality_analysis_report.md # Comprehensive 10-section scientific report
│   └── component_statistics.csv      # Statistical summaries across 24 components
├── web/
│   ├── index.html           # Interactive web dashboard interface
│   ├── app.js               # Plotly.js visualization controller
│   └── style.css            # Responsive dark-mode styling
├── main_pipeline.py         # Master pipeline orchestrator
├── test.py                  # Automated unit test suite
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```
