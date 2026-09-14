"""
Automated Unit Testing Suite for Air Quality & CPCB NAQI Analytical Platform
Tests CPCB piecewise linear sub-index formulas, health risk categories,
minimum validity criteria, and dominant pollutant identification.
"""

import unittest
import numpy as np
import pandas as pd
from pipeline.aqi_engine import calculate_sub_index, get_aqi_category, compute_aqi_dataset
from pipeline.preprocessing import get_season, preprocess_air_quality

class TestCPCBSubIndexCalculation(unittest.TestCase):
    """Verifies official CPCB NAQI piecewise linear interpolation equations."""

    def test_pm25_breakpoints(self):
        # PM2.5 Breakpoints: (0, 30)->(0, 50), (30, 60)->(51, 100), (60, 90)->(101, 200), (90, 120)->(201, 300), (120, 250)->(301, 400), (250, 500)->(401, 500)
        self.assertEqual(calculate_sub_index(0, 'PM2.5'), 0.0)
        self.assertEqual(calculate_sub_index(30, 'PM2.5'), 50.0)
        self.assertEqual(calculate_sub_index(60, 'PM2.5'), 100.0)
        self.assertEqual(calculate_sub_index(90, 'PM2.5'), 200.0)
        self.assertEqual(calculate_sub_index(120, 'PM2.5'), 300.0)
        self.assertEqual(calculate_sub_index(250, 'PM2.5'), 400.0)
        self.assertEqual(calculate_sub_index(500, 'PM2.5'), 500.0)

    def test_pm10_breakpoints(self):
        # PM10 Breakpoints: (0, 50)->(0, 50), (50, 100)->(51, 100), (100, 250)->(101, 200)
        self.assertEqual(calculate_sub_index(0, 'PM10'), 0.0)
        self.assertEqual(calculate_sub_index(50, 'PM10'), 50.0)
        self.assertEqual(calculate_sub_index(100, 'PM10'), 100.0)
        self.assertEqual(calculate_sub_index(250, 'PM10'), 200.0)

    def test_gaseous_pollutants(self):
        # NO2: 40 -> 50, 80 -> 100
        self.assertEqual(calculate_sub_index(40, 'NO2'), 50.0)
        self.assertEqual(calculate_sub_index(80, 'NO2'), 100.0)
        # CO: 1.0 -> 50, 2.0 -> 100
        self.assertEqual(calculate_sub_index(1.0, 'CO'), 50.0)
        self.assertEqual(calculate_sub_index(2.0, 'CO'), 100.0)
        # SO2: 40 -> 50, 80 -> 100
        self.assertEqual(calculate_sub_index(40, 'SO2'), 50.0)
        self.assertEqual(calculate_sub_index(80, 'SO2'), 100.0)

    def test_edge_cases(self):
        # Negative concentration
        self.assertTrue(np.isnan(calculate_sub_index(-5.0, 'PM2.5')))
        # NaN concentration
        self.assertTrue(np.isnan(calculate_sub_index(np.nan, 'PM2.5')))
        # Unknown pollutant
        self.assertTrue(np.isnan(calculate_sub_index(50, 'UNKNOWN_GAS')))
        # Extreme values beyond highest breakpoint (extrapolation)
        extreme_pm25 = calculate_sub_index(600, 'PM2.5')
        self.assertGreater(extreme_pm25, 500.0)
        self.assertLessEqual(extreme_pm25, 999.0)

class TestAQICategories(unittest.TestCase):
    """Verifies category boundaries mapping."""

    def test_category_mapping(self):
        self.assertEqual(get_aqi_category(25), "Good")
        self.assertEqual(get_aqi_category(50), "Good")
        self.assertEqual(get_aqi_category(51), "Satisfactory")
        self.assertEqual(get_aqi_category(100), "Satisfactory")
        self.assertEqual(get_aqi_category(101), "Moderate")
        self.assertEqual(get_aqi_category(200), "Moderate")
        self.assertEqual(get_aqi_category(201), "Poor")
        self.assertEqual(get_aqi_category(300), "Poor")
        self.assertEqual(get_aqi_category(301), "Very Poor")
        self.assertEqual(get_aqi_category(400), "Very Poor")
        self.assertEqual(get_aqi_category(401), "Severe")
        self.assertEqual(get_aqi_category(520), "Severe")
        self.assertEqual(get_aqi_category(np.nan), "Unknown")

class TestPreprocessingAndSeasons(unittest.TestCase):
    """Verifies meteorological season classification and environmental ratios."""

    def test_seasons(self):
        self.assertEqual(get_season(1), "Winter")
        self.assertEqual(get_season(4), "Summer")
        self.assertEqual(get_season(7), "Monsoon")
        self.assertEqual(get_season(10), "Post-Monsoon")

    def test_ratios(self):
        sample_data = {
            "Timestamp": ["2023-01-01", "2023-07-01"],
            "PM2.5": [120.0, 30.0],
            "PM10": [200.0, 60.0],
            "NO2": [50.0, 20.0],
            "NH3": [10.0, 5.0],
            "SO2": [15.0, 8.0],
            "CO": [1.2, 0.5],
            "Ozone": [40.0, 35.0],
            "Benzene": [2.0, 0.8],
            "Toluene": [4.0, 1.6],
            "Xylene": [1.0, 0.5],
            "WS": [1.5, 3.2],
            "AT": [12.0, 28.0]
        }
        df = pd.DataFrame(sample_data)
        prep = preprocess_air_quality(df)
        
        # Check PM ratio
        self.assertAlmostEqual(prep.loc[0, 'PM2.5_PM10_ratio'], 0.6, places=2)
        self.assertAlmostEqual(prep.loc[1, 'PM2.5_PM10_ratio'], 0.5, places=2)
        # Check Toluene/Benzene ratio
        self.assertAlmostEqual(prep.loc[0, 'Toluene_Benzene_ratio'], 2.0, places=2)
        # Check BTX Total
        self.assertAlmostEqual(prep.loc[0, 'BTX_Total'], 7.0, places=2)

class TestAQIDatasetComputation(unittest.TestCase):
    """Verifies multi-pollutant dataset processing and dominant pollutant selection."""

    def test_dominant_pollutant_and_composite(self):
        sample = pd.DataFrame([{
            "Timestamp": "2023-11-15",
            "PM2.5": 250.0,  # Sub-index: 400.0
            "PM10": 100.0,   # Sub-index: 100.0
            "NO2": 40.0,     # Sub-index: 50.0
            "NH3": 20.0,     # Sub-index: 5.0
            "SO2": 20.0,
            "CO": 0.8,
            "Ozone": 30.0
        }])
        res = compute_aqi_dataset(sample)
        self.assertAlmostEqual(res.loc[0, 'AQI'], 400.0, delta=1.0)
        self.assertEqual(res.loc[0, 'Dominant_Pollutant'], 'PM2.5')
        self.assertEqual(res.loc[0, 'AQI_Category'], 'Very Poor')

if __name__ == '__main__':
    unittest.main()
