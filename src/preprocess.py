import pandas as pd
import numpy as np

def _season(month):
    if month in [12, 1, 2]: return "Winter"
    if month in [3, 4, 5]: return "Summer"
    if month in [6, 7, 8, 9]: return "Monsoon"
    return "Post-Monsoon"

def preprocess(df):
    df = df.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Month_Name'] = df['Timestamp'].dt.strftime('%b')
    df['Day'] = df['Timestamp'].dt.day
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    df['Is_Weekend'] = df['Timestamp'].dt.dayofweek.isin([5, 6]).astype(int)
    df['Season'] = pd.Categorical(
        df['Month'].apply(_season),
        categories=["Winter", "Summer", "Monsoon", "Post-Monsoon"],
        ordered=True
    )
    df['PM2.5_PM10_ratio'] = np.where(
        (df['PM10'] > 0) & df['PM2.5'].notna() & df['PM10'].notna(),
        (df['PM2.5'] / df['PM10']).clip(0, 1.0), np.nan
    )
    df['BTX_Total'] = df[['Benzene', 'Toluene', 'Xylene']].sum(axis=1, skipna=False)
    df['Toluene_Benzene_ratio'] = np.where(
        (df['Benzene'] > 0) & df['Toluene'].notna() & df['Benzene'].notna(),
        df['Toluene'] / df['Benzene'], np.nan
    )
    df['Ventilation_Index_Proxy'] = np.where(
        df['WS'].notna() & df['AT'].notna(),
        df['WS'] * (df['AT'] + 273.15) / 100.0, np.nan
    )
    criteria = ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone']
    df['Valid_Criteria_Count'] = df[criteria].notna().sum(axis=1)
    df['Has_PM'] = df['PM2.5'].notna() | df['PM10'].notna()
    df['Is_AQI_Valid_Day'] = (df['Valid_Criteria_Count'] >= 3) & df['Has_PM']
    return df
