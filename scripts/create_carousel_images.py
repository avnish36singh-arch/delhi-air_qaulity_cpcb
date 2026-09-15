"""
Renders 7 standalone high-resolution (1200x1200) Instagram / LinkedIn Carousel images.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

OUT_DIR = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\carousel_images"
os.makedirs(OUT_DIR, exist_ok=True)

DELHI_PLOTS = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots"
KANPUR_PLOTS = r"C:\Users\avnis\Kanpur-LST-Thermal-Analysis-GIS\outputs\plots"

BG_COLOR = "#0B0F19"
CARD_COLOR = "#141B2D"
BORDER_COLOR = "#1E293B"
TEXT_WHITE = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
CYAN = "#06B6D4"
GREEN = "#10B981"
ORANGE = "#F97316"
PURPLE = "#A855F7"

def base_slide(slide_num, total_slides=7):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=120)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top brand bar
    ax.text(6, 93, "SIGNAL EARTH", fontsize=15, fontweight='bold', color=CYAN, fontfamily='DejaVu Sans')
    ax.text(32, 93, "// ENVIRONMENTAL OBSERVATORY", fontsize=13, fontweight='bold', color=TEXT_MUTED, fontfamily='DejaVu Sans')
    
    # Slide tracker badge
    badge = patches.FancyBboxPatch((84, 91), 10, 4, boxstyle="round,pad=0.5", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
    ax.add_patch(badge)
    ax.text(89, 92.5, f"{slide_num}/{total_slides}", fontsize=11, fontweight='bold', color=TEXT_WHITE, ha='center', va='center')

    # Bottom swipe indicator
    ax.plot([6, 94], [7, 7], color=BORDER_COLOR, lw=1.2)
    ax.text(6, 4, "RESEARCH SUITE // MULTI-YEAR ATMOSPHERIC INVESTIGATION", fontsize=9.5, color=TEXT_MUTED)
    if slide_num < total_slides:
        ax.text(94, 4, "SWIPE ➔", fontsize=10, fontweight='bold', color=CYAN, ha='right')
    else:
        ax.text(94, 4, "LINK IN BIO ➔", fontsize=10, fontweight='bold', color=GREEN, ha='right')

    return fig, ax

def embed_image(ax, img_path, extent):
    """extent = [xmin, xmax, ymin, ymax] in 0-100 coordinates"""
    if os.path.exists(img_path):
        img = Image.open(img_path)
        ax.imshow(img, extent=extent, aspect='auto', zorder=2)
        # Outer card frame
        border = patches.Rectangle((extent[0], extent[2]), extent[1]-extent[0], extent[3]-extent[2],
                                   fc='none', ec=BORDER_COLOR, lw=1.5, zorder=3)
        ax.add_patch(border)

# ----------------- SLIDE 1: COVER -----------------
def make_slide_1():
    fig, ax = base_slide(1)
    
    # Glowing category pill
    pill = patches.FancyBboxPatch((6, 81), 44, 5, boxstyle="round,pad=0.5", fc="#083344", ec=CYAN, lw=1.2)
    ax.add_patch(pill)
    ax.text(28, 83.2, "EMPIRICAL RESEARCH RELEASE", fontsize=11, fontweight='bold', color="#67E8F9", ha='center', va='center')

    ax.text(6, 73, "Decoding the\nNorth Indian Airshed", fontsize=34, fontweight='bold', color=TEXT_WHITE, linespacing=1.15)
    ax.text(6, 56, "Beyond surface averages: 5+ years of statutory\nCPCB telemetry, diagnostic chemical ratios, and\nsatellite Land Surface Temperature thermodynamics.",
            fontsize=15, color=TEXT_MUTED, linespacing=1.4)

    # 3 Stat cards across bottom
    stats = [
        ("1,825", "Daily Observations\n(2017–2023)", CYAN),
        ("78.8%", "Unhealthy Days\n(AQI > 100)", ORANGE),
        ("ΔT < 0", "Winter Inversion\nCap (< 250m)", PURPLE)
    ]
    for i, (val, desc, col) in enumerate(stats):
        x = 6 + i * 30
        card = patches.FancyBboxPatch((x, 15), 28, 25, boxstyle="round,pad=1", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.5)
        ax.add_patch(card)
        ax.text(x + 14, 32, val, fontsize=24, fontweight='bold', color=col, ha='center', va='center')
        ax.text(x + 14, 21, desc, fontsize=11.5, color=TEXT_WHITE, ha='center', va='center', linespacing=1.2)

    out = os.path.join(OUT_DIR, "slide_01_cover.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 2: THE SCALE & REALITY -----------------
def make_slide_2():
    fig, ax = base_slide(2)

    ax.text(6, 83, "The Scale of the Airshed Crisis", fontsize=25, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 78, "Delhi NCR continuous monitoring across 1,137 statutory valid days (2017–2023)", fontsize=12, color=TEXT_MUTED)

    # Embed Figure 1 time series
    embed_image(ax, os.path.join(DELHI_PLOTS, "01_aqi_time_series.png"), [6, 94, 38, 74])

    # 3 summary callout boxes
    points = [
        ("Mean AQI: 221.0 ± 123", "Classified as 'Poor' on average, not clean baseline.", ORANGE),
        ("78.80% Violations", "896 days breach the clean air threshold (AQI > 100).", "#EF4444"),
        ("36.15% Hazardous", "411 days spike into Very Poor or Severe (AQI > 300).", PURPLE)
    ]
    for i, (head, sub, col) in enumerate(points):
        x = 6 + i * 30
        card = patches.FancyBboxPatch((x, 12), 28, 22, boxstyle="round,pad=0.8", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
        ax.add_patch(card)
        ax.text(x + 14, 26, head, fontsize=12.5, fontweight='bold', color=col, ha='center', va='center')
        ax.text(x + 14, 18, sub, fontsize=10.5, color=TEXT_MUTED, ha='center', va='center', linespacing=1.3)

    out = os.path.join(OUT_DIR, "slide_02_scale_and_reality.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 3: CHEMICAL FORENSICS -----------------
def make_slide_3():
    fig, ax = base_slide(3)

    ax.text(6, 83, "Chemical Fingerprints & Hegemony", fontsize=25, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 78, "Diagnosing dominant criteria drivers and volatile organic aromatic tracers", fontsize=12, color=TEXT_MUTED)

    # Embed Figure 4 dominant pollutants & Figure 5 PM/BTEX
    embed_image(ax, os.path.join(DELHI_PLOTS, "04_dominant_pollutants.png"), [6, 48, 28, 73])
    embed_image(ax, os.path.join(DELHI_PLOTS, "05_pm_and_btex_dynamics.png"), [52, 94, 28, 73])

    # Insight box
    card = patches.FancyBboxPatch((6, 11), 88, 14, boxstyle="round,pad=0.8", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
    ax.add_patch(card)
    ax.text(9, 21, "[CHEMICAL DIAGNOSTICS] KEY FINDINGS", fontsize=11, fontweight='bold', color=CYAN)
    ax.text(9, 15, "• Particulate Hegemony: PM2.5 (51.8%) & PM10 (43.4%) trigger 95.2% of all maximum daily AQI determinations.\n• Industrial Solvents: Toluene-to-Benzene ratio regularly exceeds 3.0, proving major solvent printing/coating evaporative emissions.",
            fontsize=10.5, color=TEXT_WHITE, linespacing=1.35)

    out = os.path.join(OUT_DIR, "slide_03_chemical_forensics.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 4: KANPUR LST THERMODYNAMICS -----------------
def make_slide_4():
    fig, ax = base_slide(4)

    ax.text(6, 83, "Space-Borne Physics: The LST Inversion Trap", fontsize=25, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 78, "2,556 continuous days (2017–2023) of NASA POWER MERRA-2 thermal reanalysis", fontsize=12, color=TEXT_MUTED)

    embed_image(ax, os.path.join(KANPUR_PLOTS, "02_skin_vs_air_temperature_anomaly.png"), [6, 48, 28, 73])
    embed_image(ax, os.path.join(KANPUR_PLOTS, "01_kanpur_lst_seasonal_timeline.png"), [52, 94, 28, 73])

    # Inversion Explanation Card
    card = patches.FancyBboxPatch((6, 11), 88, 14, boxstyle="round,pad=0.8", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
    ax.add_patch(card)
    ax.text(9, 21, "[THERMODYNAMICS] THE SEASONAL INVERSION FLIP (ΔT = T_skin - T_air)", fontsize=11, fontweight='bold', color=PURPLE)
    ax.text(9, 15, "• Summer Superheating (+1.01°C): Strong solar irradiance creates convective mixing up to 2,000m, venting pollutants.\n• Winter Radiative Cooling (-0.97°C): Rapid nocturnal IR radiation loss drops ground skin below air, capping the boundary layer < 250m.",
            fontsize=10.5, color=TEXT_WHITE, linespacing=1.35)

    out = os.path.join(OUT_DIR, "slide_04_lst_inversion_trap.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 5: QGIS SPATIAL MICROCLIMATES -----------------
def make_slide_5():
    fig, ax = base_slide(5)

    ax.text(6, 83, "Urban Microclimates Modeled in QGIS", fontsize=25, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 78, "Spatial thermal anomalies modeled across industrial, vegetative, and river corridors", fontsize=12, color=TEXT_MUTED)

    embed_image(ax, os.path.join(KANPUR_PLOTS, "03_kanpur_spatial_thermal_zones.png"), [6, 48, 28, 73])
    embed_image(ax, os.path.join(KANPUR_PLOTS, "04_lst_inversion_coupling_pm25.png"), [52, 94, 28, 73])

    # Microclimate zones callout
    zones = [
        ("Urban Core", "+2.1°C UHI Trap", ORANGE),
        ("Jajmau Industrial", "+1.8°C Anomaly", "#EAB308"),
        ("IITK Canopy", "-0.8°C Cooling Buffer", GREEN),
        ("Ganga Basin", "-2.4°C Cooling Sink", CYAN)
    ]
    for i, (zname, zstat, zcol) in enumerate(zones):
        x = 6 + i * 22.5
        c = patches.FancyBboxPatch((x, 12), 21, 13, boxstyle="round,pad=0.6", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
        ax.add_patch(c)
        ax.text(x + 10.5, 20.5, zname, fontsize=11, fontweight='bold', color=TEXT_WHITE, ha='center')
        ax.text(x + 10.5, 15.5, zstat, fontsize=10, fontweight='bold', color=zcol, ha='center')

    out = os.path.join(OUT_DIR, "slide_05_spatial_microclimates.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 6: 24-HR MACHINE LEARNING FORECASTING -----------------
def make_slide_6():
    fig, ax = base_slide(6)

    ax.text(6, 83, "Predictive Machine Learning (24-Hr Ahead)", fontsize=25, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 78, "Out-of-time prospective testing on calendar year 2023 with zero temporal leakage", fontsize=12, color=TEXT_MUTED)

    embed_image(ax, os.path.join(DELHI_PLOTS, "08_forecast_evaluation.png"), [6, 94, 34, 74])

    # ML Score cards
    ml_metrics = [
        ("R² = 0.769", "Random Forest Score", GREEN),
        ("RMSE = 54.98", "Index Deviation", CYAN),
        ("62.2% Accuracy", "Health Band Categorization", ORANGE)
    ]
    for i, (val, lbl, col) in enumerate(ml_metrics):
        x = 6 + i * 30
        card = patches.FancyBboxPatch((x, 12), 28, 18, boxstyle="round,pad=0.8", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
        ax.add_patch(card)
        ax.text(x + 14, 23, val, fontsize=18, fontweight='bold', color=col, ha='center', va='center')
        ax.text(x + 14, 16.5, lbl, fontsize=11, color=TEXT_MUTED, ha='center', va='center')

    out = os.path.join(OUT_DIR, "slide_06_predictive_ml.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

# ----------------- SLIDE 7: OPEN SCIENCE PLATFORM -----------------
def make_slide_7():
    fig, ax = base_slide(7)

    # Glowing pill
    pill = patches.FancyBboxPatch((6, 82), 36, 4.5, boxstyle="round,pad=0.5", fc="#064E3B", ec=GREEN, lw=1.2)
    ax.add_patch(pill)
    ax.text(24, 84.2, "100% OPEN SOURCE SCIENCE", fontsize=10.5, fontweight='bold', color="#6EE7B7", ha='center', va='center')

    ax.text(6, 74, "Signal Earth Research Suite", fontsize=30, fontweight='bold', color=TEXT_WHITE)
    ax.text(6, 68, "Explore our reproducible computational pipelines and peer-level scientific documentation:", fontsize=12.5, color=TEXT_MUTED)

    repos = [
        ("Delhi NCR Atmospheric Telemetry Pipeline", "github.com/avnish36singh-arch/delhi-air_qaulity_cpcb",
         "1,825 continuous records | CPCB piecewise interpolation | ML forecasting engine", CYAN),
        ("Kanpur Satellite LST & QGIS Analysis", "github.com/avnish36singh-arch/Kanpur-LST-Thermal-Analysis-GIS",
         "2,556 NASA POWER daily observations | Boundary layer inversion modeling | Vector GIS", PURPLE),
        ("Signal Earth Interactive Web Observatory", "github.com/avnish36singh-arch/signal-earth-portal",
         "Unified environmental data portal, public telemetry charts, and scientific reports", GREEN)
    ]

    for i, (title, link, desc, col) in enumerate(repos):
        y = 48 - i * 16
        card = patches.FancyBboxPatch((6, y), 88, 13.5, boxstyle="round,pad=0.8", fc=CARD_COLOR, ec=BORDER_COLOR, lw=1.2)
        ax.add_patch(card)
        ax.text(9, y + 9.5, title, fontsize=13, fontweight='bold', color=col)
        ax.text(9, y + 5.5, link, fontsize=11, fontweight='bold', color=TEXT_WHITE)
        ax.text(9, y + 2, desc, fontsize=10, color=TEXT_MUTED)

    # Call to action
    ax.text(50, 11, "Save & Share to advance open environmental engineering", fontsize=12.5, fontweight='bold', color=TEXT_WHITE, ha='center')

    out = os.path.join(OUT_DIR, "slide_07_open_science.png")
    fig.savefig(out, dpi=120)
    plt.close()
    print(f"Rendered: {out}")

if __name__ == "__main__":
    make_slide_1()
    make_slide_2()
    make_slide_3()
    make_slide_4()
    make_slide_5()
    make_slide_6()
    make_slide_7()
    print("All 7 carousel post images successfully created!")
