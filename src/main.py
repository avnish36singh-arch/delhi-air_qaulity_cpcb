import os, json
import pandas as pd
import numpy as np
from src.ingest import ingest
from src.preprocess import preprocess
from src.engine import compute_aqi
from src.visualizer import generate_all_visualizations

COMPONENTS_24 = [
    "PM2.5","PM10","NO","NO2","NOx","NH3","SO2","CO","Ozone",
    "Benzene","Toluene","Xylene","O_Xylene","Eth_Benzene","MP_Xylene",
    "AT","RH","WS","WD","RF","TOT_RF","SR","BP","VWS"
]

NAAQS = {'PM2.5':60,'PM10':100,'NO2':80,'NH3':400,'SO2':80,'CO':2,'Ozone':100,'Benzene':5}

def component_stats(df):
    rows = []
    for c in COMPONENTS_24:
        s = df[c]
        v = s.notna().sum()
        if v == 0:
            continue
        lim = NAAQS.get(c)
        rows.append({
            "Component": c,
            "Valid_Days": int(v),
            "Missing_%": round((len(s) - v) / len(s) * 100, 2),
            "Mean": round(s.mean(), 2),
            "Std": round(s.std(), 2),
            "Median": round(s.median(), 2),
            "Min": round(s.min(), 2),
            "Max": round(s.max(), 2),
            "P95": round(s.quantile(0.95), 2),
            "NAAQS_Limit": lim if lim else "N/A",
            "Exceedance_%": round((s > lim).sum() / v * 100, 2) if lim else "N/A",
            "AQI_Correlation": round(df[[c, 'AQI']].dropna().corr().iloc[0, 1], 3) if 'AQI' in df.columns else "N/A"
        })
    return pd.DataFrame(rows)

def run(base_dir):
    raw_dir = os.path.join(base_dir, "data", "raw")
    proc_dir = os.path.join(base_dir, "data", "processed")
    out_dir = os.path.join(base_dir, "outputs")
    plots_dir = os.path.join(out_dir, "plots")
    data_dir = os.path.join(out_dir, "data")
    reports_dir = os.path.join(base_dir, "reports")

    os.makedirs(proc_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print("[1/5] Ingesting...")
    df = ingest(raw_dir, os.path.join(proc_dir, "air_quality_staged.csv"))

    print("[2/5] Preprocessing...")
    df = preprocess(df)

    print("[3/5] Computing AQI...")
    df = compute_aqi(df)
    df.to_csv(os.path.join(proc_dir, "air_quality_clean.csv"), index=False)

    print("[4/5] Exporting JSON...")
    json_path = os.path.join(data_dir, "cleaned.json")
    records = json.loads(df.to_json(orient="records", date_format="iso"))
    with open(json_path, "w") as f:
        json.dump(records, f, indent=2, default=str)
    print(f"  -> {json_path}")

    stats = component_stats(df)
    stats.to_csv(os.path.join(reports_dir, "component_statistics.csv"), index=False)

    print("[5/5] Generating plots...")
    generate_all_visualizations(df, plots_dir)

    print("Pipeline complete!")
    return df

if __name__ == "__main__":
    run(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
