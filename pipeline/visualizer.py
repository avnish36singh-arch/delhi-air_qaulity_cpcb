"""
Stage 4: Data Visualization Suite
Generates high-resolution, publication-grade analytical figures using Seaborn and Matplotlib.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set global visual aesthetics
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

AQI_CATEGORY_COLORS = {
    "Good": "#009966",
    "Satisfactory": "#84CC16",
    "Moderate": "#EAB308",
    "Poor": "#F97316",
    "Very Poor": "#EF4444",
    "Severe": "#7E22CE"
}

def plot_aqi_time_series(df, output_path):
    """Plots multi-year daily AQI with moving averages and CPCB category threshold bands."""
    plot_df = df[df['AQI'].notna()].copy()
    plot_df['Rolling_7D'] = plot_df['AQI'].rolling(7, min_periods=1).mean()
    plot_df['Rolling_30D'] = plot_df['AQI'].rolling(30, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(16, 7), dpi=300)

    # Background CPCB category bands
    ax.axhspan(0, 50, color='#009966', alpha=0.12, label='Good (0-50)')
    ax.axhspan(50, 100, color='#84CC16', alpha=0.12, label='Satisfactory (51-100)')
    ax.axhspan(100, 200, color='#EAB308', alpha=0.12, label='Moderate (101-200)')
    ax.axhspan(200, 300, color='#F97316', alpha=0.12, label='Poor (201-300)')
    ax.axhspan(300, 400, color='#EF4444', alpha=0.12, label='Very Poor (301-400)')
    ax.axhspan(400, 600, color='#7E22CE', alpha=0.12, label='Severe (401+)')

    # Daily AQI points and trendlines
    ax.scatter(plot_df['Timestamp'], plot_df['AQI'], color='#475569', alpha=0.35, s=16, label='Daily AQI')
    ax.plot(plot_df['Timestamp'], plot_df['Rolling_7D'], color='#2563EB', linewidth=1.8, label='7-Day Rolling Avg')
    ax.plot(plot_df['Timestamp'], plot_df['Rolling_30D'], color='#DC2626', linewidth=2.4, label='30-Day Trendline')

    ax.set_title("Multi-Year Air Quality Index (AQI) Trajectory & Health Thresholds", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("Date", fontsize=13, labelpad=10)
    ax.set_ylabel("Air Quality Index (AQI)", fontsize=13, labelpad=10)
    ax.set_ylim(0, 550)
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, ncol=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_correlation_heatmap(df, output_path):
    """Plots a 24x24 correlation matrix across all chemical and meteorological components."""
    components = [
        "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO", "Ozone",
        "Benzene", "Toluene", "Xylene", "O_Xylene", "Eth_Benzene", "MP_Xylene",
        "AT", "RH", "WS", "WD", "RF", "TOT_RF", "SR", "BP", "VWS"
    ]
    corr = df[components].corr()

    fig, ax = plt.subplots(figsize=(18, 14), dpi=300)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1.0, vmax=1.0, center=0,
                square=True, linewidths=0.6, cbar_kws={"shrink": 0.75, "label": "Pearson Correlation Coefficient"},
                annot=True, fmt=".2f", annot_kws={"size": 7.5}, ax=ax)

    ax.set_title("Inter-Component Correlation Matrix: 24 Air Quality & Meteorological Factors", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_seasonal_aqi_dynamics(df, output_path):
    """Plots seasonal distributions and boxplots of AQI."""
    plot_df = df[df['AQI'].notna()].copy()
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

    # Boxplot
    sns.boxplot(data=plot_df, x='Season', y='AQI', order=season_order, palette='Set2', ax=ax1, width=0.5, fliersize=3)
    ax1.set_title("AQI Variation Across Indian Seasons", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Season", fontsize=12)
    ax1.set_ylabel("Air Quality Index (AQI)", fontsize=12)
    ax1.axhline(100, color='green', linestyle='--', label='Satisfactory (100)')
    ax1.axhline(200, color='orange', linestyle='--', label='Moderate/Poor (200)')
    ax1.axhline(300, color='red', linestyle='--', label='Very Poor (300)')
    ax1.axhline(400, color='purple', linestyle='--', label='Severe (400)')
    ax1.legend(loc='upper left', fontsize=9)

    # Category Proportions Stacked Bar
    cat_order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    prop_df = pd.crosstab(plot_df['Season'], plot_df['AQI_Category'], normalize='index')[cat_order] * 100
    
    colors = [AQI_CATEGORY_COLORS[c] for c in cat_order]
    prop_df.loc[season_order].plot(kind='bar', stacked=True, color=colors, ax=ax2, edgecolor='white', width=0.6)
    ax2.set_title("Seasonal Composition of AQI Health Categories (%)", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Season", fontsize=12)
    ax2.set_ylabel("Percentage of Days (%)", fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.legend(title="AQI Category", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_dominant_pollutants(df, output_path):
    """Plots the primary driving pollutants that trigger peak AQI."""
    plot_df = df[df['AQI'].notna()].copy()
    counts = plot_df['Dominant_Pollutant'].value_counts()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # Donut Chart
    palette = ['#DC2626', '#EA580C', '#0284C7', '#16A34A']
    wedges, texts, autotexts = ax1.pie(
        counts, labels=counts.index, autopct='%1.1f%%', startangle=140,
        colors=palette[:len(counts)], wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    ax1.set_title("Dominant Pollutant Share in AQI Determination", fontsize=14, fontweight='bold')

    # Dominant Pollutant by Season
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]
    cross_df = pd.crosstab(plot_df['Season'], plot_df['Dominant_Pollutant'])
    cross_df.loc[season_order].plot(kind='bar', ax=ax2, color=palette[:len(counts)], width=0.6, edgecolor='white')
    ax2.set_title("Seasonal Distribution of Primary Triggering Pollutant", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Season", fontsize=12)
    ax2.set_ylabel("Number of Days", fontsize=12)
    ax2.legend(title="Dominant Pollutant", frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_pm_and_btex_dynamics(df, output_path):
    """Analyzes PM2.5/PM10 ratio and BTEX VOC distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

    # 1. PM2.5/PM10 Ratio distribution by Season
    plot_df = df[df['PM2.5_PM10_ratio'].notna()].copy()
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]
    sns.kdeplot(data=plot_df, x='PM2.5_PM10_ratio', hue='Season', hue_order=season_order,
                common_norm=False, palette='bright', fill=True, alpha=0.25, ax=ax1)
    ax1.set_title("Distribution of PM2.5 / PM10 Fine Fraction Ratio", fontsize=14, fontweight='bold')
    ax1.set_xlabel("PM2.5 / PM10 Ratio", fontsize=12)
    ax1.set_ylabel("Density", fontsize=12)
    ax1.axvline(0.5, color='gray', linestyle=':', label='Equal Fine/Coarse Threshold (0.5)')
    ax1.legend(loc='upper right', frameon=True)

    # 2. BTEX VOCs Boxplot
    btex_cols = ['Benzene', 'Toluene', 'Xylene']
    btex_melt = df.melt(id_vars=['Season'], value_vars=btex_cols, var_name='VOC', value_name='Concentration')
    btex_melt = btex_melt[btex_melt['Concentration'].notna() & (btex_melt['Concentration'] < 100)]
    
    sns.boxplot(data=btex_melt, x='VOC', y='Concentration', hue='Season', hue_order=season_order,
                palette='Set3', ax=ax2, showfliers=False)
    ax2.set_title("BTEX Volatile Organic Compounds by Season (µg/m³)", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Hydrocarbon Species", fontsize=12)
    ax2.set_ylabel("Concentration (µg/m³)", fontsize=12)
    ax2.legend(title="Season", frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_meteorology_impact(df, output_path):
    """Plots regression relationships between meteorological drivers and AQI."""
    plot_df = df[df['AQI'].notna()].copy()

    fig, axes = plt.subplots(2, 2, figsize=(15, 12), dpi=300)

    # 1. Temperature vs AQI
    sns.regplot(data=plot_df, x='AT', y='AQI', ax=axes[0, 0], scatter_kws={'alpha': 0.3, 'color': '#0284C7'}, line_kws={'color': '#DC2626'})
    axes[0, 0].set_title("Ambient Temperature vs AQI (Inversion Effect)", fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel("Ambient Temperature (°C)")
    axes[0, 0].set_ylabel("AQI")

    # 2. Wind Speed vs AQI
    sns.regplot(data=plot_df, x='WS', y='AQI', ax=axes[0, 1], scatter_kws={'alpha': 0.3, 'color': '#16A34A'}, line_kws={'color': '#DC2626'})
    axes[0, 1].set_title("Wind Speed vs AQI (Ventilation & Dispersion)", fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel("Wind Speed (m/s)")
    axes[0, 1].set_ylabel("AQI")

    # 3. Relative Humidity vs AQI
    sns.regplot(data=plot_df, x='RH', y='AQI', ax=axes[1, 0], scatter_kws={'alpha': 0.3, 'color': '#D97706'}, line_kws={'color': '#DC2626'})
    axes[1, 0].set_title("Relative Humidity vs AQI (Aerosol Condensation)", fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel("Relative Humidity (%)")
    axes[1, 0].set_ylabel("AQI")

    # 4. Solar Radiation vs Ozone
    sns.regplot(data=plot_df[plot_df['Ozone'].notna()], x='SR', y='Ozone', ax=axes[1, 1], scatter_kws={'alpha': 0.3, 'color': '#9333EA'}, line_kws={'color': '#DC2626'})
    axes[1, 1].set_title("Solar Radiation vs Tropospheric Ozone (Photochemistry)", fontsize=13, fontweight='bold')
    axes[1, 1].set_xlabel("Solar Radiation (W/m²)")
    axes[1, 1].set_ylabel("Ozone (µg/m³)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def plot_monthly_aqi_heatmap(df, output_path):
    """Year x Month matrix heatmap showing multi-year monthly average AQI."""
    plot_df = df[df['AQI'].notna()].copy()
    pivot = plot_df.pivot_table(index='Year', columns='Month', values='AQI', aggfunc='mean')
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot.columns = [month_names[m - 1] for m in pivot.columns]

    fig, ax = plt.subplots(figsize=(14, 5), dpi=300)
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Mean Monthly AQI'}, linewidths=1.0, ax=ax)
    ax.set_title("Multi-Year Monthly Average AQI Heatmap", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Year", fontsize=12)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def generate_all_visualizations(df, output_dir):
    """Orchestrates creation of all visual assets."""
    os.makedirs(output_dir, exist_ok=True)
    plot_aqi_time_series(df, os.path.join(output_dir, "01_aqi_time_series.png"))
    plot_correlation_heatmap(df, os.path.join(output_dir, "02_correlation_matrix_24_components.png"))
    plot_seasonal_aqi_dynamics(df, os.path.join(output_dir, "03_seasonal_aqi_dynamics.png"))
    plot_dominant_pollutants(df, os.path.join(output_dir, "04_dominant_pollutants.png"))
    plot_pm_and_btex_dynamics(df, os.path.join(output_dir, "05_pm_and_btex_dynamics.png"))
    plot_meteorology_impact(df, os.path.join(output_dir, "06_meteorology_impact.png"))
    plot_monthly_aqi_heatmap(df, os.path.join(output_dir, "07_monthly_aqi_heatmap.png"))
    print(f"All 7 figures generated successfully in {output_dir}!")

if __name__ == "__main__":
    clean_csv = r"c:\Users\avnis\enviornment_rajivgangulaly\data\processed\air_quality_clean.csv"
    out_dir = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots"
    df = pd.read_csv(clean_csv)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    generate_all_visualizations(df, out_dir)
