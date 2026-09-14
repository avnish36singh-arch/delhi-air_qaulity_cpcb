"""
Stage 2: Preprocessing, Data Cleansing & Environmental Feature Engineering
Cleans the staged air quality data, computes temporal features, pollutant ratios, and atmospheric indices.
"""

import pandas as pd
import numpy as np

def get_season(month):
    """Classifies month into standard Indian meteorological seasons."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

def preprocess_air_quality(df):
    """Applies comprehensive data cleaning and feature engineering to the air quality dataset."""
    df = df.copy()
    
    # 1. Temporal feature engineering
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Month_Name'] = df['Timestamp'].dt.strftime('%b')
    df['Day'] = df['Timestamp'].dt.day
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    df['Is_Weekend'] = df['Timestamp'].dt.dayofweek.isin([5, 6]).astype(int)
    df['Season'] = df['Month'].apply(get_season)
    
    # Order seasons categorically
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]
    df['Season'] = pd.Categorical(df['Season'], categories=season_order, ordered=True)
    
    # 2. Environmental & Diagnostic Ratios
    # PM2.5 to PM10 ratio: Indicates combustion/fine aerosols (<0.4: coarse dust; >0.6: combustion/smog)
    df['PM2.5_PM10_ratio'] = np.where(
        (df['PM10'] > 0) & (df['PM2.5'].notna()) & (df['PM10'].notna()),
        df['PM2.5'] / df['PM10'],
        np.nan
    )
    # Clip physical anomaly where PM2.5 > PM10 due to measurement noise
    df['PM2.5_PM10_ratio'] = df['PM2.5_PM10_ratio'].clip(0, 1.0)
    
    # Total BTX (Benzene + Toluene + Xylene) volatile organic compounds
    df['BTX_Total'] = df[['Benzene', 'Toluene', 'Xylene']].sum(axis=1, skipna=False)
    
    # Toluene / Benzene ratio: ~1.5 - 2.5 is typical vehicular exhaust, > 3.0 suggests solvent/industrial emissions
    df['Toluene_Benzene_ratio'] = np.where(
        (df['Benzene'] > 0) & (df['Toluene'].notna()) & (df['Benzene'].notna()),
        df['Toluene'] / df['Benzene'],
        np.nan
    )
    
    # Ventilation proxy index (Wind Speed * Ambient Temperature Kelvin proxy)
    df['Ventilation_Index_Proxy'] = np.where(
        df['WS'].notna() & df['AT'].notna(),
        df['WS'] * (df['AT'] + 273.15) / 100.0,
        np.nan
    )
    
    # 3. Data Quality Flag: Count monitored pollutants per day
    criteria_cols = ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone']
    df['Valid_Criteria_Count'] = df[criteria_cols].notna().sum(axis=1)
    df['Has_PM'] = (df['PM2.5'].notna() | df['PM10'].notna())
    df['Is_AQI_Valid_Day'] = (df['Valid_Criteria_Count'] >= 3) & df['Has_PM']
    
    return df

if __name__ == "__main__":
    staged_path = r"c:\Users\avnis\enviornment_rajivgangulaly\data\processed\air_quality_staged.csv"
    df = pd.read_csv(staged_path)
    clean_df = preprocess_air_quality(df)
    print("Preprocessing successful!")
    print(f"Total records: {len(clean_df)}")
    print(f"Valid AQI monitoring days: {clean_df['Is_AQI_Valid_Day'].sum()} of {len(clean_df)}")
    print("Seasonal distribution:")
    print(clean_df['Season'].value_counts())
