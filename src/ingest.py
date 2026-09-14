import os, glob
import pandas as pd
import numpy as np

STANDARD_COLUMNS = [
    "Timestamp",
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO", "Ozone",
    "Benzene", "Toluene", "Xylene", "O_Xylene", "Eth_Benzene", "MP_Xylene",
    "AT", "RH", "WS", "WD", "RF", "TOT_RF", "SR", "BP", "VWS"
]

def _parse_date(val):
    if pd.isna(val):
        return pd.NaT
    s = str(val).strip()
    try:
        parts = s.split(' ')[0].split('-')
        if len(parts[0]) == 4:
            return pd.to_datetime(s, format='%Y-%m-%d %H:%M:%S', errors='coerce')
        return pd.to_datetime(s, format='%d-%m-%Y', errors='coerce')
    except Exception:
        return pd.to_datetime(s, errors='coerce')

def _load_file(filepath):
    df = pd.read_csv(filepath, skipinitialspace=True)
    if len(df.columns) == len(STANDARD_COLUMNS):
        df.columns = STANDARD_COLUMNS
    else:
        cols = [c.strip() for c in df.columns]
        cols[0] = "Timestamp"
        df.columns = cols[:len(df.columns)]
    df.replace(['NA', 'na', 'Na', 'N/A', 'n/a', ' ', '', 'NULL', 'null'], np.nan, inplace=True)
    df['Timestamp'] = df['Timestamp'].apply(_parse_date)
    for col in STANDARD_COLUMNS[1:]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def ingest(raw_dir, output_file=None):
    files = sorted(glob.glob(os.path.join(raw_dir, "air_quality_*.csv")))
    if not files:
        raise FileNotFoundError(f"No raw files found in {raw_dir}")
    combined = pd.concat([_load_file(f) for f in files], ignore_index=True)
    combined.sort_values("Timestamp", inplace=True)
    combined.drop_duplicates(subset=["Timestamp"], keep="last", inplace=True)
    combined.reset_index(drop=True, inplace=True)
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined.to_csv(output_file, index=False)
    return combined
