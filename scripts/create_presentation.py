"""
Generates the Signal Earth Research Suite PPTX presentation
and standalone 1200x1200 high-resolution carousel post images.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_pptx(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    bg_dark = RGBColor(11, 15, 25)       # #0B0F19
    card_bg = RGBColor(20, 27, 45)       # #141B2D
    text_white = RGBColor(248, 250, 252) # #F8FAFC
    text_muted = RGBColor(148, 163, 184) # #94A3B8
    accent_cyan = RGBColor(6, 182, 212)  # #06B6D4
    accent_green = RGBColor(16, 185, 129)# #10B981
    accent_orange = RGBColor(249, 115, 22)# #F97316

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_dark
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, subtitle):
        # Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = accent_cyan

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = text_white

        # Subtitle
        if subtitle:
            tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.4))
            p_sub = tb_sub.text_frame.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = text_muted

    # ---------------- SLIDE 1: Title Slide ----------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(3.8))
    tf = tb.text_frame
    p0 = tf.paragraphs[0]
    p0.text = "SIGNAL EARTH // ENVIRONMENTAL RESEARCH SUITE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = accent_cyan

    p1 = tf.add_paragraph()
    p1.text = "Atmospheric Telemetry, Statutory NAQI & Satellite LST Thermodynamics"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = text_white
    p1.space_before = Pt(15)

    p2 = tf.add_paragraph()
    p2.text = "Multi-Year Computational Investigation Across the Indo-Gangetic Basin (2017–2023)\nFeaturing Central Pollution Control Board (CPCB) Formulations & NASA POWER Reanalysis"
    p2.font.size = Pt(16)
    p2.font.color.rgb = text_muted
    p2.space_before = Pt(20)

    # ---------------- SLIDE 2: Results at a Glance ----------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Executive Briefing", "Macro Findings & Empirical Metrics", "Summary statistics evaluated across continuous multi-year observation windows")

    metrics = [
        ("1,825 Days", "Total Timespan", "5 Complete Years (2017-18, 2021-23) continuous daily monitoring telemetry"),
        ("221.0 AQI", "Mean Airshed Level", "Classifies as 'Poor' health band across 1,137 CPCB statutory valid days"),
        ("78.80%", "Non-Compliant Days", "Exceed acceptable threshold (AQI > 100); 36.15% in Very Poor or Severe"),
        ("95.20%", "Particulate Hegemony", "PM2.5 (51.8%) and PM10 (43.4%) trigger peak sub-index determinations"),
        ("R² = 0.769", "24-hr Ahead Forecast", "Random Forest Regressor prospective validation on out-of-time test year 2023"),
        ("ΔT Inversion", "Radiant Decoupling", "Winter skin drops -0.97°C below air, capping boundary layer below 250m")
    ]

    for i, (val, label, desc) in enumerate(metrics):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(2.0 + row * 2.4)
        
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.color.rgb = RGBColor(30, 41, 69)

        tb_card = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(3.3), Inches(1.8))
        tf_c = tb_card.text_frame
        p_v = tf_c.paragraphs[0]
        p_v.text = val
        p_v.font.size = Pt(24)
        p_v.font.bold = True
        p_v.font.color.rgb = accent_green if i != 2 else accent_orange

        p_l = tf_c.add_paragraph()
        p_l.text = label
        p_l.font.size = Pt(14)
        p_l.font.bold = True
        p_l.font.color.rgb = text_white

        p_d = tf_c.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = text_muted
        p_d.space_before = Pt(5)

    # ---------------- SLIDE 3: Delhi Time Series ----------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Delhi NCR Atmospheric Pipeline", "Multi-Year AQI Trajectory & CPCB Health Bands", "Reindexed daily time series removing multi-year bridging artifacts")
    
    img_path1 = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots\01_aqi_time_series.png"
    if os.path.exists(img_path1):
        s3.shapes.add_picture(img_path1, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.1))

    # ---------------- SLIDE 4: Chemical Diagnostics ----------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Chemical Forensics", "Particulate Hegemony & Volatile Organic Tracers", "Dominant pollutant breakdown and diagnostic emission ratios")

    img_path4 = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots\04_dominant_pollutants.png"
    img_path5 = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots\05_pm_and_btex_dynamics.png"
    if os.path.exists(img_path4):
        s4.shapes.add_picture(img_path4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1))
    if os.path.exists(img_path5):
        s4.shapes.add_picture(img_path5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))

    # ---------------- SLIDE 5: Correlation Matrix ----------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Multi-Parameter Correlation", "Inter-Component Coupling Across 19 Parameters", "Pearson correlation matrix trimmed of 100% missing sensor channels")

    img_path2 = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots\02_correlation_matrix_19_components.png"
    if os.path.exists(img_path2):
        s5.shapes.add_picture(img_path2, Inches(1.8), Inches(1.8), Inches(9.7), Inches(5.2))

    # ---------------- SLIDE 6: Kanpur LST Thermodynamics ----------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Remote Sensing & Thermodynamics", "Kanpur Land Surface Temperature (LST) & Inversion", "7-Year Climatology (2017–2023) NASA POWER MERRA-2 skin-to-air thermal gradient")

    lst_img1 = r"C:\Users\avnis\Kanpur-LST-Thermal-Analysis-GIS\outputs\plots\01_kanpur_lst_seasonal_timeline.png"
    lst_img2 = r"C:\Users\avnis\Kanpur-LST-Thermal-Analysis-GIS\outputs\plots\02_skin_vs_air_temperature_anomaly.png"
    if os.path.exists(lst_img1) and os.path.exists(lst_img2):
        s6.shapes.add_picture(lst_img1, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
        s6.shapes.add_picture(lst_img2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))

    # ---------------- SLIDE 7: QGIS Spatial Microclimates ----------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Geospatial Modeling", "QGIS 3.x Vector Thermal Microclimate Zoning", "Kanpur Urban Heat Island anomalies (+2.1°C) vs vegetative cooling (-0.8°C)")

    lst_img3 = r"C:\Users\avnis\Kanpur-LST-Thermal-Analysis-GIS\outputs\plots\03_kanpur_spatial_thermal_zones.png"
    lst_img4 = r"C:\Users\avnis\Kanpur-LST-Thermal-Analysis-GIS\outputs\plots\04_lst_inversion_coupling_pm25.png"
    if os.path.exists(lst_img3) and os.path.exists(lst_img4):
        s7.shapes.add_picture(lst_img3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
        s7.shapes.add_picture(lst_img4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))

    # ---------------- SLIDE 8: Machine Learning Forecasting ----------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Predictive Machine Learning", "24-Hour Ahead AQI Forecasting & Feature Importance", "Out-of-time prospective testing on calendar year 2023 with zero data leakage")

    ml_img = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\plots\08_forecast_evaluation.png"
    if os.path.exists(ml_img):
        s8.shapes.add_picture(ml_img, Inches(1.8), Inches(1.8), Inches(9.7), Inches(5.2))

    # ---------------- SLIDE 9: Open Science ----------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Open Environmental Science", "Signal Earth Open-Source Repository Architecture", "Fully reproducible data pipelines, GIS vectors, and scientific documentation")

    tb_end = s9.shapes.add_textbox(Inches(1.5), Inches(2.4), Inches(10.3), Inches(4))
    tf_end = tb_end.text_frame
    
    repos = [
        ("Delhi NCR Atmospheric Telemetry Pipeline", "github.com/avnish36singh-arch/delhi-air_qaulity_cpcb", "1,825 daily records | CPCB piecewise interpolation | 24 parameters | ML forecast"),
        ("Kanpur Satellite LST & QGIS Analysis", "github.com/avnish36singh-arch/Kanpur-LST-Thermal-Analysis-GIS", "2,556 daily NASA POWER records | Boundary layer inversion modeling | QGIS thermal vectors"),
        ("Signal Earth Environmental Portal", "github.com/avnish36singh-arch/signal-earth-portal", "Unified environmental dashboard, documentation suite, and observatory UI")
    ]
    
    for title, url, desc in repos:
        p_t = tf_end.add_paragraph()
        p_t.text = f"• {title}"
        p_t.font.size = Pt(18)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_cyan
        p_t.space_before = Pt(14)
        
        p_u = tf_end.add_paragraph()
        p_u.text = f"  {url}"
        p_u.font.size = Pt(14)
        p_u.font.color.rgb = accent_green
        
        p_d = tf_end.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = text_muted

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_pptx = r"c:\Users\avnis\enviornment_rajivgangulaly\outputs\presentation\Signal_Earth_Research_Suite.pptx"
    create_pptx(out_pptx)
