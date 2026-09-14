"""
Stage 3: CPCB National Air Quality Index (NAQI) Calculation Engine
Computes pollutant sub-indices, composite AQI, health categories, and dominant pollutants
according to Indian Central Pollution Control Board (CPCB) standards.
"""

import numpy as np
import pandas as pd

# CPCB Breakpoint definitions: (C_low, C_high, I_low, I_high)
BREAKPOINTS = {
    'PM2.5': [
        (0.0, 30.0, 0, 50),
        (30.0, 60.0, 51, 100),
        (60.0, 90.0, 101, 200),
        (90.0, 120.0, 201, 300),
        (120.0, 250.0, 301, 400),
        (250.0, 500.0, 401, 500)
    ],
    'PM10': [
        (0.0, 50.0, 0, 50),
        (50.0, 100.0, 51, 100),
        (100.0, 250.0, 101, 200),
        (250.0, 350.0, 201, 300),
        (350.0, 430.0, 301, 400),
        (430.0, 600.0, 401, 500)
    ],
    'NO2': [
        (0.0, 40.0, 0, 50),
        (40.0, 80.0, 51, 100),
        (80.0, 180.0, 101, 200),
        (180.0, 280.0, 201, 300),
        (280.0, 400.0, 301, 400),
        (400.0, 600.0, 401, 500)
    ],
    'NH3': [
        (0.0, 200.0, 0, 50),
        (200.0, 400.0, 51, 100),
        (400.0, 800.0, 101, 200),
        (800.0, 1200.0, 201, 300),
        (1200.0, 1800.0, 301, 400),
        (1800.0, 2500.0, 401, 500)
    ],
    'SO2': [
        (0.0, 40.0, 0, 50),
        (40.0, 80.0, 51, 100),
        (80.0, 380.0, 101, 200),
        (380.0, 800.0, 201, 300),
        (800.0, 1600.0, 301, 400),
        (1600.0, 2400.0, 401, 500)
    ],
    'CO': [
        (0.0, 1.0, 0, 50),
        (1.0, 2.0, 51, 100),
        (2.0, 10.0, 101, 200),
        (10.0, 17.0, 201, 300),
        (17.0, 34.0, 301, 400),
        (34.0, 50.0, 401, 500)
    ],
    'Ozone': [
        (0.0, 50.0, 0, 50),
        (50.0, 100.0, 51, 100),
        (100.0, 168.0, 101, 200),
        (168.0, 208.0, 201, 300),
        (208.0, 748.0, 301, 400),
        (748.0, 1000.0, 401, 500)
    ]
}

def calculate_sub_index(conc, pollutant):
    """Calculates CPCB sub-index for a given pollutant concentration."""
    if pd.isna(conc) or conc < 0:
        return np.nan
        
    bp_list = BREAKPOINTS.get(pollutant)
    if not bp_list:
        return np.nan
        
    for c_low, c_high, i_low, i_high in bp_list:
        if c_low <= conc <= c_high:
            sub_index = ((i_high - i_low) / (c_high - c_low)) * (conc - c_low) + i_low
            return round(sub_index, 1)
            
    # Beyond highest breakpoint (Severe extrapolation)
    c_low, c_high, i_low, i_high = bp_list[-1]
    if conc > c_high:
        sub_index = i_high + ((i_high - i_low) / (c_high - c_low)) * (conc - c_high)
        return round(min(sub_index, 999.0), 1)
        
    return np.nan

def get_aqi_category(aqi):
    """Maps AQI numerical value to official CPCB health risk category."""
    if pd.isna(aqi):
        return "Unknown"
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

# CPCB Standard Category Color Mapping
AQI_COLORS = {
    "Good": "#009966",          # Green
    "Satisfactory": "#99CC00",  # Light green / Lime
    "Moderate": "#FFDE33",      # Yellow
    "Poor": "#FF9933",          # Orange
    "Very Poor": "#CC0033",     # Red
    "Severe": "#660099",        # Maroon / Purple
    "Unknown": "#CCCCCC"        # Grey
}

def compute_aqi_dataset(df):
    """Computes all sub-indices, composite AQI, dominant pollutant, and health categories."""
    df = df.copy()
    pollutants = list(BREAKPOINTS.keys())
    
    # Calculate sub-indices for each criteria pollutant
    for p in pollutants:
        sub_col = f"SubIndex_{p}"
        if p in df.columns:
            df[sub_col] = df[p].apply(lambda val: calculate_sub_index(val, p))
        else:
            df[sub_col] = np.nan
        
    sub_index_cols = [f"SubIndex_{p}" for p in pollutants]
    
    # CPCB Rule: At least 3 criteria pollutants with at least one particulate matter (PM2.5 or PM10)
    def compute_row_aqi(row):
        valid_subs = {p: row[f"SubIndex_{p}"] for p in pollutants if pd.notna(row[f"SubIndex_{p}"])}
        has_pm = pd.notna(row.get("SubIndex_PM2.5")) or pd.notna(row.get("SubIndex_PM10"))
        
        if len(valid_subs) >= 3 and has_pm:
            max_p = max(valid_subs, key=valid_subs.get)
            return valid_subs[max_p], max_p, True
        elif len(valid_subs) > 0 and has_pm:
            max_p = max(valid_subs, key=valid_subs.get)
            return valid_subs[max_p], max_p, False
        return np.nan, "None", False
        
    res = df.apply(compute_row_aqi, axis=1)
    df['AQI'] = [r[0] for r in res]
    df['Dominant_Pollutant'] = [r[1] for r in res]
    df['AQI_Official'] = [r[2] for r in res]
    df['AQI_Category'] = df['AQI'].apply(get_aqi_category)
    
    cat_order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe", "Unknown"]
    df['AQI_Category'] = pd.Categorical(df['AQI_Category'], categories=cat_order, ordered=True)
    
    return df

if __name__ == "__main__":
    from preprocessing import preprocess_air_quality
    staged_path = r"c:\Users\avnis\enviornment_rajivgangulaly\data\processed\air_quality_staged.csv"
    raw_df = pd.read_csv(staged_path)
    clean_df = preprocess_air_quality(raw_df)
    aqi_df = compute_aqi_dataset(clean_df)
    
    out_path = r"c:\Users\avnis\enviornment_rajivgangulaly\data\processed\air_quality_clean.csv"
    aqi_df.to_csv(out_path, index=False)
    print(f"AQI calculation complete and saved to: {out_path}")
    print("\nAQI Category Summary across monitored period:")
    print(aqi_df['AQI_Category'].value_counts())
    print("\nDominant Pollutant Distribution:")
    print(aqi_df[aqi_df['AQI'].notna()]['Dominant_Pollutant'].value_counts())
