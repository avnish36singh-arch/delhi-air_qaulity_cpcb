"""
Master Pipeline Script: End-to-End Air Quality & AQI Analytical Engine
Executes data ingestion, preprocessing, CPCB NAQI calculation, statistical reporting, and visual generation.
"""

import os
import sys
import pandas as pd
import numpy as np

import json
from pipeline.data_ingestion import ingest_all_raw_data
from pipeline.preprocessing import preprocess_air_quality
from pipeline.aqi_engine import compute_aqi_dataset
from pipeline.visualizer import generate_all_visualizations
from pipeline.forecasting import train_and_evaluate_forecast
from pipeline.source_apportionment import run_source_analysis

# 24 Air Quality and Meteorological Components
COMPONENTS_24 = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO", "Ozone",
    "Benzene", "Toluene", "Xylene", "O_Xylene", "Eth_Benzene", "MP_Xylene",
    "AT", "RH", "WS", "WD", "RF", "TOT_RF", "SR", "BP", "VWS"
]

# CPCB National Ambient Air Quality Standards (24-hr NAAQS limits where applicable)
NAAQS_LIMITS = {
    'PM2.5': 60.0,      # µg/m³
    'PM10': 100.0,      # µg/m³
    'NO2': 80.0,        # µg/m³
    'NH3': 400.0,       # µg/m³
    'SO2': 80.0,        # µg/m³
    'CO': 2.0,          # mg/m³ (8-hr / 24-hr)
    'Ozone': 100.0,     # µg/m³ (8-hr)
    'Benzene': 5.0      # µg/m³ (Annual standard reference)
}

def compute_component_statistics(df, output_path=None):
    """Calculates rigorous statistical profiles for all 24 components."""
    stats_list = []
    
    for comp in COMPONENTS_24:
        s = df[comp]
        valid_count = s.notna().sum()
        total_count = len(s)
        missing_pct = round((total_count - valid_count) / total_count * 100, 2)
        
        mean_val = round(s.mean(), 2) if valid_count > 0 else np.nan
        std_val = round(s.std(), 2) if valid_count > 0 else np.nan
        median_val = round(s.median(), 2) if valid_count > 0 else np.nan
        min_val = round(s.min(), 2) if valid_count > 0 else np.nan
        max_val = round(s.max(), 2) if valid_count > 0 else np.nan
        p95_val = round(s.quantile(0.95), 2) if valid_count > 0 else np.nan
        
        # NAAQS Exceedance rate
        limit = NAAQS_LIMITS.get(comp)
        if limit and valid_count > 0:
            exceed_count = (s > limit).sum()
            exceed_pct = round((exceed_count / valid_count) * 100, 2)
        else:
            exceed_pct = np.nan
            
        # Pearson correlation with AQI
        if valid_count > 0 and 'AQI' in df.columns:
            corr_aqi = round(df[[comp, 'AQI']].dropna().corr().iloc[0, 1], 3)
        else:
            corr_aqi = np.nan
            
        stats_list.append({
            "Component": comp,
            "Valid_Days": valid_count,
            "Missing_%": missing_pct,
            "Mean": mean_val,
            "Std": std_val,
            "Median": median_val,
            "Min": min_val,
            "Max": max_val,
            "95th_Percentile": p95_val,
            "NAAQS_Limit": limit if limit else "N/A",
            "Exceedance_%": exceed_pct if pd.notna(exceed_pct) else "N/A",
            "AQI_Correlation": corr_aqi
        })
        
    stats_df = pd.DataFrame(stats_list)
    if output_path:
        stats_df.to_csv(output_path, index=False)
        print(f"Component statistical summary saved to: {output_path}")
    return stats_df

def run_pipeline(base_dir):
    """Executes the entire end-to-end data pipeline."""
    print("=" * 70)
    print("STARTING END-TO-END AIR QUALITY & AQI ANALYSIS PIPELINE")
    print("=" * 70)
    
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    outputs_dir = os.path.join(base_dir, "outputs")
    plots_dir = os.path.join(outputs_dir, "plots")
    data_dir = os.path.join(outputs_dir, "data")
    reports_dir = os.path.join(base_dir, "reports")
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    staged_csv = os.path.join(processed_dir, "air_quality_staged.csv")
    clean_csv = os.path.join(processed_dir, "air_quality_clean.csv")
    stats_csv = os.path.join(reports_dir, "component_statistics.csv")
    json_path = os.path.join(data_dir, "cleaned.json")
    
    # 1. Ingestion
    print("\n[Stage 1/7] Ingesting multi-year raw data...")
    raw_df = ingest_all_raw_data(raw_dir, staged_csv)
    
    # 2. Preprocessing
    print("\n[Stage 2/7] Preprocessing & feature engineering...")
    prep_df = preprocess_air_quality(raw_df)
    
    # 3. AQI Computation
    print("\n[Stage 3/7] Computing CPCB National Air Quality Index (NAQI)...")
    aqi_df = compute_aqi_dataset(prep_df)
    aqi_df.to_csv(clean_csv, index=False)
    print(f"Cleaned dataset with AQI saved to: {clean_csv}")
    
    # 4. Statistical Profiling
    print("\n[Stage 4/7] Generating component statistical metrics...")
    stats_df = compute_component_statistics(aqi_df, stats_csv)
    
    # 5. Visualizations
    print("\n[Stage 5/7] Rendering 300-DPI publication-grade analytical plots...")
    generate_all_visualizations(aqi_df, plots_dir)
    
    # 6. Predictive Machine Learning (24-hr AQI Forecast)
    print("\n[Stage 6/7] Training 24-hr AQI predictive machine learning models...")
    forecast_plot = os.path.join(plots_dir, "08_forecast_evaluation.png")
    forecast_metrics, forecast_df = train_and_evaluate_forecast(aqi_df, forecast_plot)
    
    # 7. Source Apportionment & Wind Rose Polar Modeling
    print("\n[Stage 7/7] Computing directional wind roses & empirical source fingerprints...")
    sources_plot = os.path.join(plots_dir, "09_wind_rose_and_sources.png")
    source_df = run_source_analysis(aqi_df, sources_plot)
    
    # Export synchronized analytical JSON feed
    print(f"\n[Export] Exporting analytical dataset to JSON format...")
    records = json.loads(source_df.to_json(orient="records", date_format="iso"))
    with open(json_path, "w") as f:
        json.dump(records, f, indent=2, default=str)
    print(f"Master analytical dataset exported to {json_path}.")
    
    print("\n" + "=" * 70)
    print("MASTER PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return source_df, stats_df, forecast_metrics

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    source_df, stats_df, forecast_metrics = run_pipeline(project_dir)
