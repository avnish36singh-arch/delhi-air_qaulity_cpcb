import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

CAT_COLORS = {"Good":"#009966","Satisfactory":"#84CC16","Moderate":"#EAB308","Poor":"#F97316","Very Poor":"#EF4444","Severe":"#7E22CE"}

def _save(fig, path):
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

def plot_aqi_time_series(df, path):
    d = df[df['AQI'].notna()].copy()
    d['R7'] = d['AQI'].rolling(7, min_periods=1).mean()
    d['R30'] = d['AQI'].rolling(30, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(16, 7), dpi=300)
    bands = [(0,50,'#009966'),(50,100,'#84CC16'),(100,200,'#EAB308'),(200,300,'#F97316'),(300,400,'#EF4444'),(400,600,'#7E22CE')]
    for y0,y1,c in bands:
        ax.axhspan(y0, y1, color=c, alpha=0.12)
    ax.scatter(d['Timestamp'], d['AQI'], color='#475569', alpha=0.35, s=16, label='Daily AQI')
    ax.plot(d['Timestamp'], d['R7'], color='#2563EB', linewidth=1.8, label='7-Day Avg')
    ax.plot(d['Timestamp'], d['R30'], color='#DC2626', linewidth=2.4, label='30-Day Trend')
    ax.set_title("AQI Trajectory & Health Thresholds", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("Date", fontsize=13)
    ax.set_ylabel("AQI", fontsize=13)
    ax.set_ylim(0, 550)
    ax.legend(loc='upper right', frameon=True, fontsize=9.5, ncol=3)
    _save(fig, path)

def plot_correlation_heatmap(df, path):
    comps = ["PM2.5","PM10","NO","NO2","NOx","NH3","SO2","CO","Ozone","Benzene","Toluene","Xylene","O_Xylene","Eth_Benzene","MP_Xylene","AT","RH","WS","WD","RF","TOT_RF","SR","BP","VWS"]
    corr = df[comps].corr()
    fig, ax = plt.subplots(figsize=(18, 14), dpi=300)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap=sns.diverging_palette(230, 20, as_cmap=True), vmin=-1, vmax=1, center=0, square=True, linewidths=0.6, cbar_kws={"shrink":0.75}, annot=True, fmt=".2f", annot_kws={"size":7.5}, ax=ax)
    ax.set_title("24-Component Correlation Matrix", fontsize=16, fontweight='bold', pad=20)
    _save(fig, path)

def plot_seasonal_aqi(df, path):
    d = df[df['AQI'].notna()].copy()
    so = ["Winter","Summer","Monsoon","Post-Monsoon"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)
    sns.boxplot(data=d, x='Season', y='AQI', order=so, palette='Set2', ax=a1, width=0.5, fliersize=3)
    a1.set_title("AQI by Season", fontsize=14, fontweight='bold')
    for y, c, l in [(100,'green','100'),(200,'orange','200'),(300,'red','300'),(400,'purple','400')]:
        a1.axhline(y, color=c, linestyle='--', label=l)
    a1.legend(fontsize=9)
    cats = ["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"]
    prop = pd.crosstab(d['Season'], d['AQI_Category'], normalize='index')[cats] * 100
    prop.loc[so].plot(kind='bar', stacked=True, color=[CAT_COLORS[c] for c in cats], ax=a2, edgecolor='white', width=0.6)
    a2.set_title("Seasonal AQI Category %", fontsize=14, fontweight='bold')
    a2.set_ylim(0, 100)
    a2.legend(title="Category", bbox_to_anchor=(1.02, 1), loc='upper left')
    _save(fig, path)

def plot_dominant_pollutants(df, path):
    d = df[df['AQI'].notna()].copy()
    counts = d['Dominant_Pollutant'].value_counts()
    pal = ['#DC2626','#EA580C','#0284C7','#16A34A']
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    a1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=pal[:len(counts)], wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    a1.set_title("Dominant Pollutant Share", fontsize=14, fontweight='bold')
    so = ["Winter","Summer","Monsoon","Post-Monsoon"]
    pd.crosstab(d['Season'], d['Dominant_Pollutant']).loc[so].plot(kind='bar', ax=a2, color=pal[:len(counts)], width=0.6, edgecolor='white')
    a2.set_title("Dominant Pollutant by Season", fontsize=14, fontweight='bold')
    a2.legend(title="Pollutant")
    _save(fig, path)

def plot_pm_btex(df, path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)
    so = ["Winter","Summer","Monsoon","Post-Monsoon"]
    d = df[df['PM2.5_PM10_ratio'].notna()].copy()
    sns.kdeplot(data=d, x='PM2.5_PM10_ratio', hue='Season', hue_order=so, common_norm=False, palette='bright', fill=True, alpha=0.25, ax=a1)
    a1.set_title("PM2.5/PM10 Ratio Distribution", fontsize=14, fontweight='bold')
    a1.axvline(0.5, color='gray', linestyle=':')
    btex = df.melt(id_vars=['Season'], value_vars=['Benzene','Toluene','Xylene'], var_name='VOC', value_name='Conc')
    btex = btex[btex['Conc'].notna() & (btex['Conc'] < 100)]
    sns.boxplot(data=btex, x='VOC', y='Conc', hue='Season', hue_order=so, palette='Set3', ax=a2, showfliers=False)
    a2.set_title("BTEX VOCs by Season (µg/m³)", fontsize=14, fontweight='bold')
    _save(fig, path)

def plot_meteorology(df, path):
    d = df[df['AQI'].notna()].copy()
    fig, axes = plt.subplots(2, 2, figsize=(15, 12), dpi=300)
    pairs = [('AT','AQI','#0284C7','Temperature vs AQI'),('WS','AQI','#16A34A','Wind Speed vs AQI'),('RH','AQI','#D97706','Humidity vs AQI')]
    for i, (x, y, c, t) in enumerate(pairs):
        ax = axes[i//2, i%2]
        sns.regplot(data=d, x=x, y=y, ax=ax, scatter_kws={'alpha':0.3,'color':c}, line_kws={'color':'#DC2626'})
        ax.set_title(t, fontsize=13, fontweight='bold')
    sns.regplot(data=d[d['Ozone'].notna()], x='SR', y='Ozone', ax=axes[1,1], scatter_kws={'alpha':0.3,'color':'#9333EA'}, line_kws={'color':'#DC2626'})
    axes[1,1].set_title("Solar Radiation vs Ozone", fontsize=13, fontweight='bold')
    _save(fig, path)

def plot_monthly_heatmap(df, path):
    d = df[df['AQI'].notna()].copy()
    pivot = d.pivot_table(index='Year', columns='Month', values='AQI', aggfunc='mean')
    pivot.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][:len(pivot.columns)]
    fig, ax = plt.subplots(figsize=(14, 5), dpi=300)
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label':'Mean AQI'}, linewidths=1.0, ax=ax)
    ax.set_title("Monthly Average AQI Heatmap", fontsize=15, fontweight='bold', pad=15)
    _save(fig, path)

def generate_all_visualizations(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    plot_aqi_time_series(df, os.path.join(output_dir, "01_aqi_time_series.png"))
    plot_correlation_heatmap(df, os.path.join(output_dir, "02_correlation_matrix.png"))
    plot_seasonal_aqi(df, os.path.join(output_dir, "03_seasonal_aqi.png"))
    plot_dominant_pollutants(df, os.path.join(output_dir, "04_dominant_pollutants.png"))
    plot_pm_btex(df, os.path.join(output_dir, "05_pm_btex.png"))
    plot_meteorology(df, os.path.join(output_dir, "06_meteorology.png"))
    plot_monthly_heatmap(df, os.path.join(output_dir, "07_monthly_heatmap.png"))
