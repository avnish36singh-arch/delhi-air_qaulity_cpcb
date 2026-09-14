import numpy as np
import pandas as pd

BREAKPOINTS = {
    'PM2.5': [(0,30,0,50),(30,60,51,100),(60,90,101,200),(90,120,201,300),(120,250,301,400),(250,500,401,500)],
    'PM10': [(0,50,0,50),(50,100,51,100),(100,250,101,200),(250,350,201,300),(350,430,301,400),(430,600,401,500)],
    'NO2': [(0,40,0,50),(40,80,51,100),(80,180,101,200),(180,280,201,300),(280,400,301,400),(400,600,401,500)],
    'NH3': [(0,200,0,50),(200,400,51,100),(400,800,101,200),(800,1200,201,300),(1200,1800,301,400),(1800,2500,401,500)],
    'SO2': [(0,40,0,50),(40,80,51,100),(80,380,101,200),(380,800,201,300),(800,1600,301,400),(1600,2400,401,500)],
    'CO': [(0,1,0,50),(1,2,51,100),(2,10,101,200),(10,17,201,300),(17,34,301,400),(34,50,401,500)],
    'Ozone': [(0,50,0,50),(50,100,51,100),(100,168,101,200),(168,208,201,300),(208,748,301,400),(748,1000,401,500)]
}

def _sub_index(conc, pollutant):
    if pd.isna(conc) or conc < 0:
        return np.nan
    bp = BREAKPOINTS.get(pollutant)
    if not bp:
        return np.nan
    for cl, ch, il, ih in bp:
        if cl <= conc <= ch:
            return round(((ih - il) / (ch - cl)) * (conc - cl) + il, 1)
    cl, ch, il, ih = bp[-1]
    if conc > ch:
        return round(min(ih + ((ih - il) / (ch - cl)) * (conc - ch), 999.0), 1)
    return np.nan

def _category(aqi):
    if pd.isna(aqi): return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Severe"

def compute_aqi(df):
    df = df.copy()
    pollutants = list(BREAKPOINTS.keys())
    for p in pollutants:
        df[f"SubIndex_{p}"] = df[p].apply(lambda v: _sub_index(v, p))

    def _row_aqi(row):
        valid = {p: row[f"SubIndex_{p}"] for p in pollutants if pd.notna(row[f"SubIndex_{p}"])}
        has_pm = pd.notna(row.get("SubIndex_PM2.5")) or pd.notna(row.get("SubIndex_PM10"))
        if valid and has_pm:
            mp = max(valid, key=valid.get)
            return valid[mp], mp
        return np.nan, "None"

    res = df.apply(_row_aqi, axis=1)
    df['AQI'] = [r[0] for r in res]
    df['Dominant_Pollutant'] = [r[1] for r in res]
    df['AQI_Category'] = pd.Categorical(
        df['AQI'].apply(_category),
        categories=["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe", "Unknown"],
        ordered=True
    )
    return df
