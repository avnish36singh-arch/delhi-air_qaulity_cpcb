import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Set visualization aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Load the processed air quality & AQI dataset
DATA_PATH = "data/processed/air_quality_clean.csv"

def load_data():
    """Loads the preprocessed air quality dataset with calculated CPCB AQI."""
    df = pd.read_csv(DATA_PATH)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

if __name__ == "__main__":
    df = load_data()
    print("=" * 65)
    print("AIR QUALITY & AQI DATASET LOADED SUCCESSFULLY")
    print("=" * 65)
    print(f"Total Observations : {len(df):,} days")
    print(f"Date Range         : {df['Timestamp'].min().strftime('%Y-%m-%d')} to {df['Timestamp'].max().strftime('%Y-%m-%d')}")
    print(f"Valid AQI Days     : {df['AQI'].notna().sum():,} days")
    print(f"Mean Multi-Year AQI: {df['AQI'].mean():.1f} ({df['AQI'].median():.1f} median)")
    
    print("\n--- AQI Health Category Distribution ---")
    valid = df[df['AQI'].notna()]
    cat_dist = valid['AQI_Category'].value_counts()
    for cat, count in cat_dist.items():
        pct = (count / len(valid)) * 100
        print(f"  {cat:<15}: {count:>4} days ({pct:>5.1f}%)")
        
    print("\n--- Dominant Pollutant Triggering Peak AQI ---")
    dom_dist = valid['Dominant_Pollutant'].value_counts()
    for pol, count in dom_dist.items():
        pct = (count / len(valid)) * 100
        print(f"  {pol:<15}: {count:>4} days ({pct:>5.1f}%)")
    print("=" * 65)