"""
Stage 6: Source Apportionment & Directional Pollution Rose Modeling
Analyzes atmospheric transport trajectories (Wind Direction) and empirical
chemical tracer ratios (PM2.5/PM10, Toluene/Benzene, CO/NOx) to fingerprint emission sources.
"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SECTOR_LABELS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

def assign_wind_sector(deg):
    """Binds wind direction degrees (0-360) into 16 cardinal sectors."""
    if pd.isna(deg):
        return np.nan
    deg = deg % 360
    idx = int((deg + 11.25) / 22.5) % 16
    return SECTOR_LABELS[idx]

def compute_source_fingerprints(df):
    """Categorizes days into primary source regimes based on chemical diagnostics."""
    data = df.copy()
    data['Wind_Sector'] = data['WD'].apply(assign_wind_sector)
    
    # Classify empirical emission regimes
    def classify_source(row):
        pm_ratio = row.get('PM2.5_PM10_ratio')
        tb_ratio = row.get('Toluene_Benzene_ratio')
        season = row.get('Season')
        
        if pd.isna(pm_ratio):
            return "Unclassified"
        if pm_ratio >= 0.65 and season in ['Winter', 'Post-Monsoon']:
            return "Biomass & Stubble Smog"
        elif pm_ratio < 0.40 and season in ['Summer', 'Monsoon']:
            return "Fugitive & Crustal Dust"
        elif tb_ratio and tb_ratio > 3.0:
            return "Industrial Solvent Emissions"
        elif 0.40 <= pm_ratio < 0.65:
            return "Vehicular & Urban Mixed"
        else:
            return "Regional Background"
            
    data['Source_Regime'] = data.apply(classify_source, axis=1)
    return data

def plot_wind_rose_and_sources(data, output_path):
    """Generates 300-DPI polar and chemical source apportionment figure."""
    fig = plt.figure(figsize=(16, 11), dpi=300)
    
    # 1. Polar Plot: PM2.5 Directional Intensity
    ax1 = fig.add_subplot(2, 2, 1, projection='polar')
    valid_wd = data[data['WD'].notna() & data['PM2.5'].notna()].copy()
    
    angles = np.linspace(0, 2 * np.pi, 17)[:-1]
    pm25_means = []
    pm10_means = []
    
    for sector in SECTOR_LABELS:
        s_data = valid_wd[valid_wd['Wind_Sector'] == sector]
        pm25_means.append(s_data['PM2.5'].mean() if len(s_data) > 0 else 0)
        pm10_means.append(s_data['PM10'].mean() if len(s_data) > 0 else 0)
        
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    ax1.plot(np.append(angles, angles[0]), np.append(pm25_means, pm25_means[0]), color='#DC2626', linewidth=2.2, label='Mean PM2.5 (µg/m³)')
    ax1.plot(np.append(angles, angles[0]), np.append(pm10_means, pm10_means[0]), color='#F97316', linewidth=1.8, linestyle='--', label='Mean PM10 (µg/m³)')
    ax1.fill(np.append(angles, angles[0]), np.append(pm25_means, pm25_means[0]), color='#DC2626', alpha=0.15)
    ax1.set_xticks(angles)
    ax1.set_xticklabels(SECTOR_LABELS, fontsize=8.5, fontweight='bold')
    ax1.set_title("Directional Particulate Matter (PM) Pollution Rose", fontsize=12, fontweight='bold', pad=15)
    ax1.legend(loc='lower right', bbox_to_anchor=(1.25, -0.05), fontsize=8.5)
    
    # 2. Polar Plot: Gaseous (NO2 & SO2) Directional Intensity
    ax2 = fig.add_subplot(2, 2, 2, projection='polar')
    valid_gas = data[data['WD'].notna() & data['NO2'].notna() & data['SO2'].notna()].copy()
    no2_means = []
    so2_means = []
    for sector in SECTOR_LABELS:
        s_data = valid_gas[valid_gas['Wind_Sector'] == sector]
        no2_means.append(s_data['NO2'].mean() if len(s_data) > 0 else 0)
        so2_means.append(s_data['SO2'].mean() if len(s_data) > 0 else 0)
        
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    ax2.plot(np.append(angles, angles[0]), np.append(no2_means, no2_means[0]), color='#2563EB', linewidth=2.2, label='Mean NO2 (µg/m³)')
    ax2.plot(np.append(angles, angles[0]), np.append(so2_means, so2_means[0]), color='#9333EA', linewidth=1.8, linestyle='--', label='Mean SO2 (µg/m³)')
    ax2.fill(np.append(angles, angles[0]), np.append(no2_means, no2_means[0]), color='#2563EB', alpha=0.15)
    ax2.set_xticks(angles)
    ax2.set_xticklabels(SECTOR_LABELS, fontsize=8.5, fontweight='bold')
    ax2.set_title("Directional Gaseous (NO2 / SO2) Pollution Rose", fontsize=12, fontweight='bold', pad=15)
    ax2.legend(loc='lower right', bbox_to_anchor=(1.25, -0.05), fontsize=8.5)
    
    # 3. Monthly PM2.5/PM10 Combustion vs Crustal Dust Evolution
    ax3 = fig.add_subplot(2, 2, 3)
    monthly_ratio = data.groupby('Month')['PM2.5_PM10_ratio'].mean()
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    ax3.plot(month_names, monthly_ratio.values, marker='o', color='#059669', linewidth=2.4, markersize=7)
    ax3.axhspan(0.60, 1.0, color='#DC2626', alpha=0.12, label='Combustion & Biomass (>0.60)')
    ax3.axhspan(0.40, 0.60, color='#EAB308', alpha=0.12, label='Vehicular & Mixed Urban (0.40-0.60)')
    ax3.axhspan(0.0, 0.40, color='#3B82F6', alpha=0.12, label='Coarse Crustal Road Dust (<0.40)')
    ax3.set_title("Annual Cycle of Fine Particle Fraction (PM2.5 / PM10 Ratio)", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Month", fontsize=10)
    ax3.set_ylabel("PM2.5 / PM10 Ratio", fontsize=10)
    ax3.set_ylim(0.2, 0.8)
    ax3.legend(loc='lower left', fontsize=8.5)
    
    # 4. Overall Source Regime Distribution
    ax4 = fig.add_subplot(2, 2, 4)
    regimes = data['Source_Regime'].value_counts()
    regimes = regimes[regimes.index != 'Unclassified']
    colors = ['#DC2626', '#3B82F6', '#EAB308', '#8B5CF6', '#10B981']
    wedges, texts, autotexts = ax4.pie(
        regimes.values, 
        labels=regimes.index, 
        autopct='%1.1f%%', 
        colors=colors[:len(regimes)],
        startangle=140,
        textprops={'fontsize': 9}
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    ax4.set_title("Empirical Emission Source Regime Attribution", fontsize=12, fontweight='bold')
    
    plt.subplots_adjust(top=0.93, bottom=0.08, left=0.07, right=0.93, hspace=0.35, wspace=0.35)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Source apportionment visual saved to: {output_path}")

def run_source_analysis(df, output_plot_path=None):
    """Main execution function for source apportionment."""
    print("Performing empirical chemical fingerprinting and directional polar modeling...")
    data_sources = compute_source_fingerprints(df)
    if output_plot_path:
        plot_wind_rose_and_sources(data_sources, output_plot_path)
    return data_sources

if __name__ == "__main__":
    clean_csv = "data/processed/air_quality_clean.csv"
    plot_out = "outputs/plots/09_wind_rose_and_sources.png"
    if os.path.exists(clean_csv):
        df = pd.read_csv(clean_csv)
        data_sources = run_source_analysis(df, plot_out)
