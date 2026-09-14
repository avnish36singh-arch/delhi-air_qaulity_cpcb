# Comprehensive Air Quality & AQI Analytical Report
**Multi-Year Environmental, Chemical, and Meteorological Investigation (2017–2023)**  
*Conducted in accordance with Central Pollution Control Board (CPCB) NAQI Guidelines*

---

## Executive Summary

This study delivers an end-to-end analytical assessment of ambient air quality and atmospheric dynamics across five monitored calendar years (**2017, 2018, 2021, 2022, and 2023**), encompassing **1,825 daily monitoring records** and **24 environmental and meteorological parameters**. Utilizing a custom-built automated data pipeline powered by Python (`pandas`, `numpy`, `matplotlib`, and `seaborn`), the system standardized heterogeneous monitoring schemas, engineered seasonal and chemical diagnostic features, computed official piecewise linear **CPCB National Air Quality Index (NAQI)** sub-indices and composite values, and mapped cross-parameter correlations.

### High-Level Environmental Findings

| Metric | Empirical Value | Context & Environmental Interpretation |
| :--- | :--- | :--- |
| **Total Monitored Days** | 1,825 days | 5 complete calendar years (2017–2018, 2021–2023) |
| **Days with Valid CPCB AQI** | 1,138 days (62.4%) | Evaluated against CPCB minimum criteria (≥3 pollutants including PM) |
| **Mean Composite AQI** | **221.23 ± 123.17** | Categorized as **Poor** on average |
| **Median Composite AQI** | **205.10** | Over 50% of valid days exceed the acceptable threshold |
| **AQI Range (Min – Max)** | **23.70 – 523.40** | Extreme dynamic range: Clean monsoon washout to severe hazardous smog |
| **Unhealthy Days (AQI > 100)** | **897 days (78.82%)** | Moderate, Poor, Very Poor, or Severe air quality |
| **Hazardous Days (AQI > 300)** | **412 days (36.20%)** | Over 1 in 3 days poses acute severe health risks |
| **Clean / Acceptable Days (AQI ≤ 100)** | **241 days (21.18%)** | Confined almost exclusively to the peak monsoon months (July–Sept) |
| **Primary Driver Pollutant** | **$PM_{2.5}$ (51.8%) & $PM_{10}$ (43.5%)** | Particulate matter accounts for **95.26%** of all dominant AQI episodes |

```
                       AQI Category Distribution (% of Valid Days)
┌──────────────────────────────────────────────────────────────────────────┐
│ [Good: 4.75%] [Satisfactory: 16.43%] [Moderate: 28.30%]                  │
│ [Poor: 14.32%]       [Very Poor: 27.68%]              [Severe: 8.52%]    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 1. CPCB National Air Quality Index (NAQI) Methodology

The Central Pollution Control Board (CPCB) of India defines the National Air Quality Index (NAQI) to translate complex multi-pollutant concentrations into a single numerical index reflecting public health risk.

### Piecewise Linear Breakpoint Interpolation

For any criteria pollutant $p$ with measured daily concentration $C_p$, the sub-index $I_p$ is calculated using the breakpoint equation:

$$I_p = \frac{I_{hi} - I_{lo}}{B_{hi} - B_{lo}} \times (C_p - B_{lo}) + I_{lo}$$

where:
- $B_{hi}$ and $B_{lo}$ represent the upper and lower concentration breakpoints for the category enclosing $C_p$.
- $I_{hi}$ and $I_{lo}$ represent the corresponding index breakpoints.

### CPCB Concentration Breakpoint Table

| Category | AQI Range | $PM_{2.5}$ ($\mu g/m^3$) | $PM_{10}$ ($\mu g/m^3$) | $NO_2$ ($\mu g/m^3$) | $NH_3$ ($\mu g/m^3$) | $SO_2$ ($\mu g/m^3$) | $CO$ ($mg/m^3$) | $O_3$ ($\mu g/m^3$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Good** | 0 – 50 | 0 – 30 | 0 – 50 | 0 – 40 | 0 – 200 | 0 – 40 | 0 – 1.0 | 0 – 50 |
| **Satisfactory** | 51 – 100 | 31 – 60 | 51 – 100 | 41 – 80 | 201 – 400 | 41 – 80 | 1.1 – 2.0 | 51 – 100 |
| **Moderate** | 101 – 200 | 61 – 90 | 101 – 250 | 81 – 180 | 401 – 800 | 81 – 380 | 2.1 – 10 | 101 – 168 |
| **Poor** | 201 – 300 | 91 – 120 | 251 – 350 | 181 – 280 | 801 – 1200 | 381 – 800 | 10.1 – 17 | 169 – 208 |
| **Very Poor** | 301 – 400 | 121 – 250 | 351 – 430 | 281 – 400 | 1201 – 1800 | 801 – 1600 | 17.1 – 34 | 209 – 748 |
| **Severe** | 401 – 500 | 250+ | 430+ | 400+ | 1800+ | 1600+ | 34+ | 748+ |

### Validation & Aggregation Rules

1. **Minimum Data Requirement**: To compute a valid daily composite AQI, at least three criteria sub-indices must be present, of which at least one must be a particulate parameter ($PM_{2.5}$ or $PM_{10}$).
2. **Composite AQI Formulation**:
   $$AQI = \max\left(I_{PM2.5}, I_{PM10}, I_{NO2}, I_{NH3}, I_{SO2}, I_{CO}, I_{O3}\right)$$
3. **Dominant Pollutant Determination**: The specific pollutant responsible for $\max(I_p)$ is assigned as the **Dominant Pollutant** for that day.

---

## 2. Statistical Profiling of All 24 Parameters

The monitoring station features 24 atmospheric parameters categorized into 15 Criteria Pollutants & Chemical Precursors and 9 Meteorological Drivers.

### Complete 24-Component Empirical Summary

| # | Parameter | Unit | Valid Days | Missing % | Mean | Std Dev | Median | Min | Max | 95th % | NAAQS Limit | Exceedance % | AQI Corr ($r$) |
| :-: | :--- | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | **$PM_{2.5}$** | $\mu g/m^3$ | 1,134 | 37.86% | 107.52 | 80.47 | 82.56 | 4.81 | 529.87 | 264.61 | 60.0 | **62.61%** | **+0.921** |
| 2 | **$PM_{10}$** | $\mu g/m^3$ | 1,135 | 37.81% | 207.46 | 116.99 | 199.02 | 11.35 | 640.19 | 420.17 | 100.0 | **78.15%** | **+0.929** |
| 3 | **$NO$** | $\mu g/m^3$ | 1,135 | 37.81% | 12.01 | 16.62 | 4.55 | 0.69 | 155.11 | 46.16 | N/A | N/A | **+0.566** |
| 4 | **$NO_2$** | $\mu g/m^3$ | 1,135 | 37.81% | 29.23 | 18.43 | 25.52 | 3.45 | 115.59 | 61.30 | 80.0 | **3.52%** | **+0.728** |
| 5 | **$NO_x$** | $ppb$ | 1,135 | 37.81% | 25.36 | 21.34 | 17.53 | 3.39 | 191.26 | 68.71 | N/A | N/A | **+0.695** |
| 6 | **$NH_3$** | $\mu g/m^3$ | 1,128 | 38.19% | 20.76 | 12.02 | 19.20 | 0.20 | 65.94 | 42.82 | 400.0 | 0.00% | +0.264 |
| 7 | **$SO_2$** | $\mu g/m^3$ | 1,121 | 38.58% | 11.83 | 7.64 | 9.37 | 2.42 | 47.10 | 26.94 | 80.0 | 0.00% | +0.443 |
| 8 | **$CO$** | $mg/m^3$ | 1,136 | 37.75% | 1.07 | 0.47 | 1.00 | 0.28 | 4.02 | 1.78 | 2.0 | **2.82%** | +0.364 |
| 9 | **$Ozone$** | $\mu g/m^3$ | 1,118 | 38.74% | 31.05 | 19.81 | 25.74 | 2.17 | 109.72 | 70.62 | 100.0 | **0.36%** | +0.164 |
| 10 | **$Benzene$** | $\mu g/m^3$ | 1,138 | 37.64% | 2.32 | 2.58 | 1.25 | 0.00 | 13.16 | 8.04 | 5.0* | **15.73%** | **+0.552** |
| 11 | **$Toluene$** | $\mu g/m^3$ | 1,138 | 37.64% | 15.28 | 16.43 | 10.08 | 0.00 | 176.23 | 43.58 | N/A | N/A | +0.467 |
| 12 | **$Xylene$** | $\mu g/m^3$ | 1,138 | 37.64% | 1.26 | 1.67 | 0.69 | 0.00 | 20.27 | 4.11 | N/A | N/A | +0.486 |
| 13 | **$O-Xylene$** | $\mu g/m^3$ | 0 | 100.0% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 14 | **$Eth-Benzene$**| $\mu g/m^3$ | 0 | 100.0% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 15 | **$MP-Xylene$** | $\mu g/m^3$ | 0 | 100.0% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 16 | **$AT$** (Temp) | °C | 1,135 | 37.81% | 24.12 | 7.55 | 25.75 | 7.78 | 38.44 | 34.31 | N/A | N/A | **-0.557** |
| 17 | **$RH$** (Humid) | % | 1,136 | 37.75% | 59.75 | 14.44 | 62.42 | 28.23 | 87.03 | 78.72 | N/A | N/A | +0.034 |
| 18 | **$WS$** (Wind) | $m/s$ | 0 | 100.0% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 19 | **$WD$** (Dir) | deg | 1,136 | 37.75% | 170.81 | 72.58 | 171.47 | 37.00 | 318.45 | 274.07 | N/A | N/A | +0.202 |
| 20 | **$RF$** (Rain) | $mm$ | 878 | 51.89% | 0.11 | 0.64 | 0.00 | 0.00 | 10.00 | 0.50 | N/A | N/A | -0.168 |
| 21 | **$TOT-RF$** | $mm$ | 1,825 | 0.00% | 0.93 | 6.88 | 0.00 | 0.00 | 169.00 | 1.00 | N/A | N/A | **-0.203** |
| 22 | **$SR$** (Solar) | $W/m^2$ | 1,136 | 37.75% | 143.47 | 56.27 | 145.74 | 4.53 | 419.48 | 233.20 | N/A | N/A | **-0.357** |
| 23 | **$BP$** (Press) | $mmHg$ | 1,136 | 37.75% | 982.38 | 8.39 | 981.91 | 963.59 | 999.44 | 994.95 | N/A | N/A | **+0.481** |
| 24 | **$VWS$** | $m/s$ | 0 | 100.0% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

*\*Note: Benzene standard is an annual threshold of 5.0 $\mu g/m^3$; 15.73% of daily observations exceeded this annual safety threshold.*

### Sensor Availability & Inactive Channel Audit
- **Fully Monitored Parameters (19 channels)**: Active daily sensor telemetry was recorded for 19 channels during 2018 (partial), 2021, 2022, and 2023. Year 2017 raw logs were placeholder entries ($TOT\_RF$ recorded, other sensors inactive prior to station commissioning).
- **Unequipped / Unlogged Channels (5 channels)**: $O-Xylene$, $Eth-Benzene$, $MP-Xylene$, $WS$ (Horizontal Wind Speed), and $VWS$ (Vertical Wind Speed) contained 100% missing values in the raw source files, indicating either uninstalled sensor pods or channel multiplexing into total $Xylene$.

---

## 3. Dominant Pollutant Dynamics & Source Fingerprinting

### Primary AQI Drivers

When evaluating which criteria sub-index dictates the overall daily AQI:
- **$PM_{2.5}$**: **51.76% of days** (589 days) — Predominantly governs late autumn, winter, and post-monsoon smog.
- **$PM_{10}$**: **43.50% of days** (495 days) — Predominantly governs pre-monsoon summer months due to crustal dust and soil suspension.
- **$CO$**: **4.39% of days** (50 days) — Intermittent spikes occurring during winter temperature inversions and stagnant traffic congestion.
- **$Ozone$**: **0.35% of days** (4 days) — Sporadic high-solar episodes in late spring / early summer.
- **$NO_2, SO_2, NH_3$**: **0.00%** — Never exceeded particulate sub-indices to become the primary driver.

```
                  Primary Pollutant Share
  PM2.5  ████████████████████████████  51.76%
  PM10   ███████████████████████       43.50%
  CO     ██                            4.39%
  Ozone  ▌                             0.35%
```

### Particulate Characterization: Fine-to-Coarse Ratio ($PM_{2.5} / PM_{10}$)

The ratio of $PM_{2.5}$ to $PM_{10}$ serves as a critical diagnostic metric for source characterization:
- **High Ratio (> 0.60)**: Direct combustion emissions, vehicular exhaust, biomass burning, and secondary aerosol synthesis.
- **Low Ratio (< 0.45)**: Mechanical grinding, construction dust, road re-suspension, and windblown crustal dust.

| Season | Mean $PM_{2.5}/PM_{10}$ | Median | Min – Max | Dominant Aerosol Genesis |
| :--- | :---: | :---: | :---: | :--- |
| **Winter (Dec–Feb)** | **0.65 ± 0.12** | **0.65** | 0.27 – 0.92 | Biomass burning, heating combustion, diesel exhaust, secondary sulfates/nitrates |
| **Post-Monsoon (Oct–Nov)** | **0.57 ± 0.13** | **0.56** | 0.26 – 1.00 | Agricultural stubble burning, festive pyrotechnics, stagnant low boundary layer |
| **Monsoon (Jun–Sep)** | **0.43 ± 0.13** | **0.41** | 0.15 – 0.94 | Wet deposition preferentially washes fine aerosols; reduced biomass burning |
| **Summer (Mar–May)** | **0.40 ± 0.10** | **0.40** | 0.10 – 0.73 | Crustal soil resuspension, construction debris, long-range dust transport |

### BTEX Hydrocarbon Fingerprinting & Toluene/Benzene Ratio

The **Toluene-to-Benzene ($T/B$) mass ratio** provides insight into hydrocarbon emission sources:
- In pure vehicular exhaust, the typical $T/B$ ratio ranges from **1.5 to 2.5**.
- Higher ratios ($T/B > 4.0$) indicate strong localized non-traffic sources, specifically printing units, paints, chemical solvent evaporation, and industrial coating facilities.
- **Observed Median $T/B$ Ratio**: **7.84** (Ranging seasonally from 5.38 in winter to 13.17 in monsoon).
- **Inference**: High toluene concentrations relative to benzene demonstrate that industrial solvent emissions, surface coatings, and evaporation significantly supplement tailpipe emissions in this airshed. Benzene itself reached a peak of $13.16\ \mu g/m^3$, heavily exceeding the $5\ \mu g/m^3$ annual benchmark on 15.73% of days.

---

## 4. Seasonal Dynamics & Synoptic Meteorology

### Seasonal AQI Profile

The airshed exhibits severe, cyclical seasonal oscillation dictated by synoptic meteorology and planetary boundary layer height.

```
Seasonal Mean AQI Comparison:
  Monsoon        (Jun–Sep) : ██████████ 104.4 (Moderate)
  Summer         (Mar–May) : █████████████████████ 215.2 (Poor)
  Post-Monsoon   (Oct–Nov) : ██████████████████████████████ 300.0 (Very Poor)
  Winter         (Dec–Feb) : ████████████████████████████████ 313.3 (Very Poor)
```

| Season | Valid Days | Mean AQI | Median AQI | Std Dev | Min | Max | Dominant Health Risk |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Monsoon** | 360 | **104.43** | 90.60 | 63.48 | 23.70 | 432.80 | Minimum (Washout periods) |
| **Summer** | 274 | **215.19** | 205.90 | 89.46 | 48.80 | 452.30 | High coarse dust exposure |
| **Post-Monsoon** | 203 | **299.96** | 322.10 | 114.41 | 27.60 | 523.40 | Severe acute episodic smog |
| **Winter** | 301 | **313.32** | 332.10 | 86.42 | 40.90 | 458.30 | Chronic severe air stagnation |

### Monthly AQI Trajectory

Monthly averages demonstrate the precise onset, intensification, and collapse of the annual pollution cycle:

| Month | Name | Valid Days | Mean AQI | Median AQI | CPCB Category | Meteorological State |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | **Jan** | 93 | **298.78** | 327.10 | Poor / Very Poor | Deep thermal inversions, shallow boundary layer (<400m) |
| 2 | **Feb** | 84 | **270.12** | 303.05 | Poor | Gradual warming, inversion breakup |
| 3 | **Mar** | 91 | **223.78** | 223.90 | Poor | Convective thermal onset |
| 4 | **Apr** | 90 | **241.99** | 244.25 | Poor | Dry, windy, high crustal dust transport |
| 5 | **May** | 93 | **180.86** | 162.70 | Moderate | Intense solar irradiance, high convective mixing |
| 6 | **Jun** | 90 | **159.93** | 139.85 | Moderate | Pre-monsoon showers, increased dispersion |
| 7 | **Jul** | 87 | **83.84** | 70.30 | **Satisfactory** | Heavy monsoon precipitation, wet scavenging |
| 8 | **Aug** | 93 | **92.28** | 94.40 | **Satisfactory** | Active southwest monsoon, low regional emissions |
| 9 | **Sep** | 90 | **81.39** | 77.15 | **Satisfactory** | Cleanest month of the annual cycle |
| 10 | **Oct** | 93 | **211.89** | 197.20 | Poor | Monsoon withdrawal, rapid cooling, stubble fires |
| 11 | **Nov** | 110 | **374.41** | **384.00** | **Very Poor / Severe** | **Annual pollution peak**, calm winds, crop residue smog |
| 12 | **Dec** | 124 | **353.49** | 359.70 | **Very Poor** | Persistent radiation fogs, cold pool subsidence |

### Meteorological Mechanisms Governing Dispersion & Accumulation

1. **Ambient Temperature Inversion ($r = -0.557$)**:
   - Temperature shows a powerful inverse correlation with AQI. During November–January, radiative surface cooling produces strong nighttime and morning ground-based thermal inversions. The nocturnal Planetary Boundary Layer (PBL) drops to below 200–400 meters, trapping primary pollutants near breathing level.
2. **Barometric Pressure Stagnation ($r = +0.481$)**:
   - Barometric pressure is strongly positively correlated with AQI. High-pressure synoptic anticyclones dominate winter, creating descending air parcels (subsidence) that suppress vertical updrafts and lock pollutants in place.
3. **Solar Radiation & Convection ($r = -0.357$)**:
   - Higher solar irradiance in spring and summer drives sensible heat flux, raising the PBL height above 2,000–3,000 meters. The resulting convective thermals dilute surface concentrations despite higher regional dust emissions.
4. **Precipitation Scavenging ($r = -0.203$)**:
   - Monsoonal precipitation effectively washes out atmospheric particulates and soluble gases via in-cloud and below-cloud wet scavenging, dropping mean AQI from 374 (November) to 81 (September).

---

## 5. Regulatory NAAQS Exceedance & Health Impact Assessment

### Compliance with Indian 24-hr NAAQS Standards

| Pollutant | CPCB NAAQS Limit | Observed Mean | Observed Peak | Days Monitored | Days Violating Standard | Non-Compliance Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$PM_{10}$** | $100\ \mu g/m^3$ | $207.46\ \mu g/m^3$ | $640.19\ \mu g/m^3$ | 1,135 | **887 days** | **78.15%** |
| **$PM_{2.5}$** | $60\ \mu g/m^3$ | $107.52\ \mu g/m^3$ | $529.87\ \mu g/m^3$ | 1,134 | **710 days** | **62.61%** |
| **$Benzene$** | $5.0\ \mu g/m^3$ | $2.32\ \mu g/m^3$ | $13.16\ \mu g/m^3$ | 1,138 | **179 days** | **15.73%** |
| **$NO_2$** | $80\ \mu g/m^3$ | $29.23\ \mu g/m^3$ | $115.59\ \mu g/m^3$ | 1,135 | **40 days** | **3.52%** |
| **$CO$** | $2.0\ mg/m^3$ | $1.07\ mg/m^3$ | $4.02\ mg/m^3$ | 1,136 | **32 days** | **2.82%** |
| **$Ozone$** | $100\ \mu g/m^3$ | $31.05\ \mu g/m^3$ | $109.72\ \mu g/m^3$ | 1,118 | **4 days** | **0.36%** |
| **$SO_2$** | $80\ \mu g/m^3$ | $11.83\ \mu g/m^3$ | $47.10\ \mu g/m^3$ | 1,121 | 0 days | **0.00%** |
| **$NH_3$** | $400\ \mu g/m^3$ | $20.76\ \mu g/m^3$ | $65.94\ \mu g/m^3$ | 1,128 | 0 days | **0.00%** |

### Public Health & Toxicological Implications

1. **Cardiovascular & Cerebrovascular Pathology ($PM_{2.5}$)**:
   - With 62.6% of days exceeding safety thresholds and peak values surpassing $500\ \mu g/m^3$, ultrafine particulates easily penetrate alveolar gas-exchange barriers into systemic circulation. This triggers endothelial dysfunction, systemic inflammation, acute myocardial infarction, and ischemic stroke.
2. **Chronic Respiratory Morbidity ($PM_{10}$ & $NO_2$)**:
   - $PM_{10}$ non-compliance (78.15%) causes persistent upper airway irritation, exacerbating chronic obstructive pulmonary disease (COPD), bronchial asthma, and pediatric respiratory infections. The co-presence of $NO_2$ enhances airway hyperresponsiveness.
3. **Oncogenic Risk from Volatile Aromatics ($Benzene$)**:
   - Benzene is an established IARC Group 1 human carcinogen with no safe threshold. The observation that 15.73% of days exceed $5\ \mu g/m^3$ represents substantial long-term hematotoxic risk, including elevated lifetime incidence of acute myeloid leukemia (AML) and aplastic anemia for nearby populations.

---

## 6. Actionable Environmental Policy & Engineering Mitigation

Based on empirical data findings, the following multi-tiered mitigation strategy is proposed:

### Tier 1: Emergency Episode Management (GRAP Integration)
- **Graded Response Action Plan (GRAP)**: Automated enforcement triggered by real-time AQI thresholds:
  - **AQI > 300 (Very Poor)**: Complete ban on diesel generator sets, 50% increase in parking fees to discourage personal vehicle usage, deployment of mechanized road vacuum sweepers with mist cannons.
  - **AQI > 400 (Severe)**: Immediate halt to construction and demolition activities, restricted entry of medium/heavy commercial diesel trucks, shifting industrial units to approved clean piped fuels (PNG).

### Tier 2: Source-Specific Engineering Interventions
1. **Fugitive & Road Dust Suppression**:
   - Address the 78.15% $PM_{10}$ exceedance by mandating green barriers along arterial roads, paving unpaved shoulders, and installing continuous water spray curtains around construction perimeters.
2. **Volatile Organic Compound (VOC) Abatement**:
   - Mitigate the high $T/B$ ratio and benzene spikes by installing Stage I and Stage II Vapor Recovery Systems (VRS) at all retail fuel outlets and mandating closed-loop solvent recovery systems in surrounding paint, printing, and automotive body shops.
3. **Vehicular Fleet Modernization**:
   - Accelerate phase-out of commercial vehicles older than 10–15 years, subsidize commercial 3-wheeler electrification, and expand low-emission mass transit corridors.

### Tier 3: Sensor Pod Upgrades & Air Quality Network Hardening
- Recommission unlogged sensor channels (**Horizontal Wind Speed, Vertical Wind Speed, and Speciated Xylenes**) to enable accurate Gaussian dispersion modeling and automated chemical mass balance source apportionment.

---

---

## 8. Predictive Machine Learning & 24-Hour Ahead Forecasting

To evaluate the operational predictability of severe air quality episodes, a supervised time-series forecasting architecture was constructed using multi-year lag features and evaluated on a true out-of-time prospective testing period (**Calendar Year 2023**).

### Model Architecture & Training Protocol
- **Training Horizon**: 773 contiguous monitored days (2018–2022).
- **Out-of-Time Testing Horizon**: 357 contiguous monitored days (2023).
- **Feature Set**: Chronological pollutant lags ($t, t-1, t-2$ of $PM_{2.5}, PM_{10}, NO_2, CO$), meteorological momentum (Temperature, Humidity, Barometric Pressure, Solar Radiation, Wind Direction), 3-day rolling mean, $PM_{2.5}/PM_{10}$ ratio, and cyclical solar harmonics ($\sin, \cos$ of day of year).

### Prospective 2023 Validation Metrics

| Model Architecture | Test $R^2$ Score | Root Mean Squared Error (RMSE) | Mean Absolute Error (MAE) | Health Category Accuracy |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest Regressor (150 trees, max_depth=8)** | **0.769** | **54.98** | **39.69** | **62.2%** |
| **Ridge Linear Baseline ($\alpha=10.0$)** | 0.764 | 55.61 | 42.40 | 60.8% |

### Key Feature Importance (Gini Impurity Reduction)
1. **$AQI_t$ (Current Day AQI)**: Strongest single predictor (persistence and atmospheric inertia).
2. **$PM_{2.5\_t}$ (Ground-level Fine Particles)**: Governs next-day particulate accumulation.
3. **$AQI_{rolling3D}$ (3-Day Moving Momentum)**: Captures multi-day synoptic stagnation episodes.
4. **$AT_t$ (Ambient Temperature)**: Inversion trigger and boundary layer dynamics.
5. **$BP_t$ (Barometric Pressure)**: High-pressure anticyclonic stagnation marker.

> **Methodological Disclosure & Gap-Handling Note**: Features are constructed strictly within each contiguous monitoring year with small gaps ($\le 2$ days) linearly interpolated; longer gaps forward/back-filled. Out-of-time prospective testing on year 2023 with zero temporal leakage.

---

## 9. Indicative Source Signature (ratio-based diagnostic) & Directional Transport Dynamics

Combining directional Wind Direction ($WD$) binning with diagnostic chemical tracer ratios provides an indicative screening diagnostic of regional emissions. *(Note: This ratio-based classification represents qualitative indicative signatures, distinct from rigorous receptor modeling such as Positive Matrix Factorization [PMF] or Chemical Mass Balance [CMB] on speciated chemical composition data).*

### 1. Directional Particulate Pollution Rose
- **Northwest to North-Northwest ($300^\circ - 330^\circ$)**: Dominates peak severe $PM_{2.5}$ concentrations during post-monsoon and early winter, aligning with regional transboundary biomass and agricultural residue plumes entering the airshed.
- **Southeast to East ($90^\circ - 140^\circ$)**: Exhibits elevated $NO_2$ and $SO_2$ loading, indicating heavy vehicular freight corridors and downwind industrial zones.

### 2. Indicative Source Signature Distribution

Methodology: Regimes are classified via fine-to-coarse particulate ratios ($PM_{2.5}/PM_{10}$) and volatile aromatic tracer ratios ($Toluene/Benzene$), gated by seasonal meteorological conditions.

| Indicative Regime | Diagnostic Criteria | Monitored Days | Share of Classified Days (%) | Primary Seasonal Phasing |
| :--- | :--- | :---: | :---: | :--- |
| **Industrial Solvent Emissions** | $Toluene/Benzene > 3.0$ | **567** | **50.1%** | Localized and regional solvent/industrial tracer loading |
| **Fugitive & Crustal Road Dust** | $PM_{2.5}/PM_{10} < 0.40$ (Summer / Monsoon) | **307** | **27.1%** | Pre-monsoon dry months & high mechanical shear |
| **Biomass & Stubble Smog** | $PM_{2.5}/PM_{10} \ge 0.65$ (Winter / Post-Monsoon) | **200** | **17.7%** | October – January acute transboundary combustion plumes |
| **Vehicular & Urban Mixed** | $0.40 \le PM_{2.5}/PM_{10} < 0.65$ | **54** | **4.8%** | Urban background traffic & tailpipe emissions |
| **Regional Background** | Baseline residual concentration | **3** | **0.3%** | Peak monsoon precipitation scavenging |

*(Total classified: 1,131 days; 694 days unclassified due to missing PM component or off-season threshold bounds).*

---

## 10. Visual Analytics Index

All publication-grade visual charts generated at 300 DPI are located in `outputs/plots/`:

1. `outputs/plots/01_aqi_time_series.png`: Multi-Year Daily AQI Timeline with CPCB Health Bands & Rolling 30-day Trajectory.
2. `outputs/plots/02_correlation_matrix_24_components.png`: Full Pearson Correlation Heatmap across all 24 parameters.
3. `outputs/plots/03_seasonal_aqi_dynamics.png`: Seasonal Boxplots and Violin Density Distributions across Seasons.
4. `outputs/plots/04_dominant_pollutants.png`: Pie and Bar Distribution of Primary Driving Pollutants.
5. `outputs/plots/05_pm_and_btex_dynamics.png`: Particulate Ratios ($PM_{2.5}/PM_{10}$) & BTEX Volatile Aromatic Trends.
6. `outputs/plots/06_meteorology_impact.png`: Meteorological Scatter Regressions (Temperature, Pressure, Radiation, Rain vs AQI).
7. `outputs/plots/07_monthly_aqi_heatmap.png`: Month vs Year Heatmap showing cyclical winter peaks and monsoon lulls.
8. `outputs/plots/08_forecast_evaluation.png`: 24-hr Ahead Predictive ML Evaluation (Observed vs Predicted Timeline & Feature Importance).
9. `outputs/plots/09_wind_rose_and_sources.png`: Directional Wind Rose Polar Plots ($PM, NO_2, SO_2$) & Indicative Source Signatures.

---
*Report compiled autonomously via the Master Air Quality & AQI Analytical Pipeline.*

