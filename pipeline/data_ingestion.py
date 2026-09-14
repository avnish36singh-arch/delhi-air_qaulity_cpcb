"""
Stage 1: Data Ingestion & Schema Alignment
Consolidates raw multi-year air quality monitoring data into a unified, clean DataFrame.
"""

import os
import glob
import pandas as pd
import numpy as np

# Standardized clean column names mapping to the 24 components
STANDARD_COLUMNS = [
    "Timestamp",
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO", "Ozone",
    "Benzene", "Toluene", "Xylene", "O_Xylene", "Eth_Benzene", "MP_Xylene",
    "AT", "RH", "WS", "WD", "RF", "TOT_RF", "SR", "BP", "VWS"
]

def load_and_standardize_file(filepath):
    """Reads a single air quality CSV file, normalizes header and formats timestamps."""
    print(f"Reading file: {filepath}")
    df = pd.read_csv(filepath, skipinitialspace=True)
    
    # Ensure 25 columns (Timestamp + 24 components)
    if len(df.columns) == len(STANDARD_COLUMNS):
        df.columns = STANDARD_COLUMNS
    else:
        # Match by position or strip special characters
        cols = [c.strip() for c in df.columns]
        # Rename timestamp
        cols[0] = "Timestamp"
        df.columns = cols[:len(df.columns)]
    
    # Clean whitespace and standard missing markers
    df.replace(['NA', 'na', 'Na', 'N/A', 'n/a', ' ', '', 'NULL', 'null'], np.nan, inplace=True)
    
    # Parse timestamp flexibly
    # 2023 format: DD-MM-YYYY, other years: YYYY-MM-DD HH:MM:SS
    def parse_date(val):
        if pd.isna(val):
            return pd.NaT
        s = str(val).strip()
        try:
            if '-' in s:
                parts = s.split(' ')[0].split('-')
                if len(parts[0]) == 4: # YYYY-MM-DD
                    return pd.to_datetime(s, format='%Y-%m-%d %H:%M:%S', errors='coerce')
                else: # DD-MM-YYYY
                    return pd.to_datetime(s, format='%d-%m-%Y', errors='coerce')
            return pd.to_datetime(s, errors='coerce')
        except Exception:
            return pd.to_datetime(s, errors='coerce')
            
    df['Timestamp'] = df['Timestamp'].apply(parse_date)
    
    # Convert numerical columns to float64
    for col in STANDARD_COLUMNS[1:]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def ingest_all_raw_data(raw_dir, output_file=None):
    """Ingests and combines all available raw year CSV files."""
    files = sorted(glob.glob(os.path.join(raw_dir, "air_quality_*.csv")))
    if not files:
        raise FileNotFoundError(f"No raw files found in {raw_dir}")
        
    dfs = []
    for f in files:
        sub_df = load_and_standardize_file(f)
        dfs.append(sub_df)
        print(f"Loaded {len(sub_df)} rows from {os.path.basename(f)}")
        
    combined = pd.concat(dfs, ignore_index=True)
    combined.sort_values(by="Timestamp", inplace=True)
    combined.drop_duplicates(subset=["Timestamp"], keep="last", inplace=True)
    combined.reset_index(drop=True, inplace=True)
    
    print(f"Total consolidated rows: {len(combined)}, covering {combined['Timestamp'].min()} to {combined['Timestamp'].max()}")
    
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined.to_csv(output_file, index=False)
        print(f"Consolidated raw data saved to: {output_file}")
        
    return combined

if __name__ == "__main__":
    raw_dir = r"c:\Users\avnis\enviornment_rajivgangulaly\data\raw"
    out_file = r"c:\Users\avnis\enviornment_rajivgangulaly\data\processed\air_quality_staged.csv"
    ingest_all_raw_data(raw_dir, out_file)
