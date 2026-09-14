"""
Stage 5: Predictive AQI Machine Learning & 24-hr Forecasting Engine
Trains supervised machine learning models with temporal lag features
and evaluates next-day AQI prediction on an out-of-time test period (2023).
"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from pipeline.aqi_engine import get_aqi_category

def create_forecasting_features(df):
    """Generates chronological lag and meteorological features within each monitoring year."""
    data = df[df["AQI"].notna()].sort_values("Timestamp").copy()
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])
    data["Year"] = data["Timestamp"].dt.year
    
    # Available informative continuous parameters
    feature_cols = ["AQI", "PM2.5", "PM10", "NO2", "CO", "AT", "RH", "BP", "SR", "WD"]
    available_cols = [c for c in feature_cols if c in data.columns and data[c].notna().sum() > 100]
    
    lagged_dfs = []
    # Process within each contiguous monitoring year to prevent cross-year leakage across gaps
    for year, group in data.groupby("Year"):
        if len(group) < 30:
            continue
        g = group.sort_values("Timestamp").copy()
        
        # Interpolate small 1-2 day gaps within the continuous year
        for col in available_cols:
            g[col] = g[col].interpolate(method="linear", limit=2).bfill().ffill()
            
        # Target: Next-day AQI (t+1)
        g["Target_AQI_Next_Day"] = g["AQI"].shift(-1)
        
        # Lags t-1 and t-2 for key pollutants and meteorology
        for col in available_cols:
            g[f"{col}_t"] = g[col]
            g[f"{col}_lag1"] = g[col].shift(1)
            g[f"{col}_lag2"] = g[col].shift(2)
            
        g["AQI_Rolling3D"] = g["AQI"].rolling(3, min_periods=1).mean()
        g["PM_Ratio_t"] = (g["PM2.5"] / g["PM10"].replace(0, np.nan)).clip(0, 1.0)
        
        # Cyclical calendar features
        doy = g["Timestamp"].dt.dayofyear
        g["Sin_DayOfYear"] = np.sin(2 * np.pi * doy / 365.25)
        g["Cos_DayOfYear"] = np.cos(2 * np.pi * doy / 365.25)
        
        # Valid rows must have valid target and lag features
        g_valid = g[g["Target_AQI_Next_Day"].notna() & g["AQI_lag1"].notna()].copy()
        lagged_dfs.append(g_valid)
        
    df_model = pd.concat(lagged_dfs, ignore_index=True)
    return df_model

def train_and_evaluate_forecast(df, output_plot_path=None):
    """Trains forecasting models and produces validation metrics and evaluation plots."""
    print("Building lag features and temporal train/test split...")
    df_feat = create_forecasting_features(df)
    
    # Temporal split: Train on years < 2023, Test on 2023 (True prospective out-of-time evaluation)
    train_df = df_feat[df_feat["Year"] < 2023].copy()
    test_df = df_feat[df_feat["Year"] == 2023].copy()
    
    ignore_cols = ["Timestamp", "Target_AQI_Next_Day", "Year", "Season", "Dominant_Pollutant", "AQI_Category"]
    candidate_features = [c for c in train_df.columns if c not in ignore_cols and not c.startswith("SubIndex_") and np.issubdtype(train_df[c].dtype, np.number)]
    
    # Keep features that have at least 50% valid values in training set
    feature_names = [c for c in candidate_features if train_df[c].notna().mean() >= 0.5]
    
    # Clean imputation using train medians
    median_vals = train_df[feature_names].median().fillna(0)
    X_train = train_df[feature_names].fillna(median_vals)
    y_train = train_df["Target_AQI_Next_Day"]
    X_test = test_df[feature_names].fillna(median_vals)
    y_test = test_df["Target_AQI_Next_Day"]
    
    # Ensure zero NaNs remain
    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)
    
    print(f"Training observations: {len(X_train)} days | Out-of-time Test (2023): {len(X_test)} days across {len(feature_names)} features")
    
    # 1. Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=150, max_depth=8, min_samples_split=4, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    # 2. Ridge Baseline
    ridge = Ridge(alpha=10.0)
    ridge.fit(X_train, y_train)
    y_pred_ridge = ridge.predict(X_test)
    
    # Metrics
    r2_rf = r2_score(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    
    r2_ridge = r2_score(y_test, y_pred_ridge)
    rmse_ridge = np.sqrt(mean_squared_error(y_test, y_pred_ridge))
    mae_ridge = mean_absolute_error(y_test, y_pred_ridge)
    
    # Health Category Accuracy
    cat_true = y_test.apply(get_aqi_category)
    cat_pred = pd.Series(y_pred_rf, index=y_test.index).apply(get_aqi_category)
    cat_acc = (cat_true == cat_pred).mean() * 100
    
    print(f"\n--- 24-hr Ahead AQI Forecast Performance (Test Year: 2023) ---")
    print(f"Random Forest Regressor : R² = {r2_rf:.3f} | RMSE = {rmse_rf:.2f} | MAE = {mae_rf:.2f}")
    print(f"Ridge Linear Baseline   : R² = {r2_ridge:.3f} | RMSE = {rmse_ridge:.2f} | MAE = {mae_ridge:.2f}")
    print(f"Category Hit Rate       : {cat_acc:.1f}%")
    
    # Feature Importances
    importances = pd.Series(rf.feature_importances_, index=feature_names).sort_values(ascending=False)
    
    metrics = {
        "RF_R2": round(r2_rf, 3),
        "RF_RMSE": round(rmse_rf, 2),
        "RF_MAE": round(mae_rf, 2),
        "Ridge_R2": round(r2_ridge, 3),
        "Ridge_RMSE": round(rmse_ridge, 2),
        "Ridge_MAE": round(mae_ridge, 2),
        "Category_Accuracy_Pct": round(cat_acc, 1),
        "Top_Features": {k: round(v, 4) for k, v in importances.head(6).items()}
    }
    
    test_df["Pred_AQI_RF"] = y_pred_rf
    test_df["Pred_Category"] = cat_pred
    test_df["True_Category"] = cat_true
    
    if output_plot_path:
        plot_forecast_evaluation(test_df, importances, metrics, output_plot_path)
        
    return metrics, test_df

def plot_forecast_evaluation(test_df, importances, metrics, output_path):
    """Renders 300-DPI publication visual summarizing predictive model performance."""
    fig = plt.figure(figsize=(16, 10), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0], hspace=0.32, wspace=0.25)
    
    # Subplot 1: 2023 Time Series: Actual vs 24-hr Predicted AQI
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axhspan(0, 50, color='#009966', alpha=0.1, label='Good (0-50)')
    ax1.axhspan(50, 100, color='#84CC16', alpha=0.1, label='Satisfactory (51-100)')
    ax1.axhspan(100, 200, color='#EAB308', alpha=0.1, label='Moderate (101-200)')
    ax1.axhspan(200, 300, color='#F97316', alpha=0.1, label='Poor (201-300)')
    ax1.axhspan(300, 400, color='#EF4444', alpha=0.1, label='Very Poor (301-400)')
    ax1.axhspan(400, 600, color='#7E22CE', alpha=0.1, label='Severe (401+)')
    
    ax1.plot(test_df["Timestamp"], test_df["Target_AQI_Next_Day"], color="#1E293B", linewidth=1.8, label="Observed Next-Day AQI (Ground Truth)")
    ax1.plot(test_df["Timestamp"], test_df["Pred_AQI_RF"], color="#2563EB", linewidth=1.8, linestyle="--", label=f"Random Forest Forecast (R² = {metrics['RF_R2']})")
    
    ax1.set_title("2023 Prospective Validation: Observed vs 24-Hour Ahead Predicted AQI", fontsize=14, fontweight='bold', pad=12)
    ax1.set_xlabel("Date (2023)", fontsize=11)
    ax1.set_ylabel("Air Quality Index (AQI)", fontsize=11)
    ax1.set_ylim(0, 530)
    ax1.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=9.5, ncol=3)
    
    # Subplot 2: Actual vs Predicted Scatter
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.scatter(test_df["Target_AQI_Next_Day"], test_df["Pred_AQI_RF"], color="#3B82F6", alpha=0.6, edgecolors="none", s=32)
    max_val = max(test_df["Target_AQI_Next_Day"].max(), test_df["Pred_AQI_RF"].max()) + 20
    lims = [0, max_val]
    ax2.plot(lims, lims, color="#DC2626", linestyle=":", linewidth=2.0, label="1:1 Perfect Prediction")
    ax2.set_xlim(lims)
    ax2.set_ylim(lims)
    ax2.set_title(f"Forecast Accuracy (R²: {metrics['RF_R2']} | RMSE: {metrics['RF_RMSE']})", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Actual Next-Day AQI", fontsize=10)
    ax2.set_ylabel("Predicted Next-Day AQI", fontsize=10)
    ax2.legend(loc="upper left", frameon=True, facecolor="white", fontsize=9)
    
    # Subplot 3: Top Feature Importances
    ax3 = fig.add_subplot(gs[1, 1])
    top_feats = importances.head(8).sort_values(ascending=True)
    y_pos = np.arange(len(top_feats))
    ax3.barh(y_pos, top_feats.values, color="#10B981", alpha=0.85, edgecolor="#059669")
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(top_feats.index, fontsize=9.5)
    ax3.set_title("Top Predictive Features (Gini Impurity Reduction)", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Relative Feature Importance Score", fontsize=10)
    
    plt.subplots_adjust(top=0.93, bottom=0.08, left=0.08, right=0.96, hspace=0.35, wspace=0.25)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Forecast evaluation visual saved to: {output_path}")

if __name__ == "__main__":
    clean_csv = "data/processed/air_quality_clean.csv"
    plot_out = "outputs/plots/08_forecast_evaluation.png"
    if os.path.exists(clean_csv):
        df = pd.read_csv(clean_csv)
        metrics, test_preds = train_and_evaluate_forecast(df, plot_out)
