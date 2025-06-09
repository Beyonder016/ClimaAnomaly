# data_collector.py

import os
import requests
import pandas as pd
from datetime import datetime
import json
import numpy as np  # if you're using np.nan instead of pd.NA

data_cache_dir = "data_cache"
os.makedirs(data_cache_dir, exist_ok=True)

# NASA POWER base URL
BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch_climate_data(lat, lon, start_date, end_date, parameters=None):
    """
    Fetch climate data from NASA POWER API and return a pandas DataFrame.
    Returns None if the fetch fails or if the data is invalid.
    """

    if parameters is None:
        parameters = ["T2M", "RH2M", "PRECTOTCORR", "ALLSKY_SFC_SW_DWN"]

    filename = f"{lat}_{lon}_{start_date}_{end_date}.csv"
    filepath = os.path.join(data_cache_dir, filename)

    if os.path.exists(filepath):
        print(f"[INFO] Loading data from cache: {filepath}")
        try:
            df = pd.read_csv(filepath, parse_dates=["DATE"])
            if df.empty or df.isna().all().all():
                print("[ERROR] Cached file exists but contains no valid data.")
                return None
            return df
        except Exception as e:
            print(f"[ERROR] Failed to read cache: {e}")
            return None

    params = {
        "parameters": ",".join(parameters),
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    print("[INFO] Fetching data from NASA POWER API...")
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"[DEBUG] Request URL: {response.url}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        data = response.json()
        print("[FULL API RESPONSE]", json.dumps(data, indent=2)[:1000])  # limit for readability
    except Exception as e:
        print(f"[ERROR] Could not fetch or parse API response: {e}")
        return None

    if "messages" in data and data["messages"]:
        print("[ERROR] API returned message:", data["messages"])
        return None

    if "properties" not in data or "parameter" not in data["properties"]:
        print("[ERROR] Missing 'properties.parameter' in response.")
        return None

    records = data["properties"]["parameter"]
    if not records:
        print("[ERROR] Parameter section is empty.")
        return None

    try:
        # Build DataFrame
        dates = list(records[list(records.keys())[0]].keys())
        df = pd.DataFrame({"DATE": pd.to_datetime(dates)})

        for param, value_map in records.items():
            df[param] = [value_map.get(date, None) for date in dates]

        print(f"[DEBUG] DataFrame shape: {df.shape}")
        print(df.head())

        # Handle case where all rows or all values are NaN
        if df.empty or df.isna().all().all():
            print("[ERROR] Final DataFrame is empty or all values are NaN.")
            return None

        # Replace -999 with NaN (NASA fill value)
        df.replace(-999, pd.NA, inplace=True)

        df.to_csv(filepath, index=False)
        print(f"[INFO] Data saved to: {filepath}")
        return df

    except Exception as e:
        print(f"[ERROR] Failed to build DataFrame: {e}")
        return None

# Test run (can be deleted in production)
if __name__ == "__main__":
    df = fetch_climate_data(
        lat=18.52,
        lon=73.86,
        start_date="20230101",
        end_date="20231231"
    )
    if df is not None:
        print("[SUCCESS] Preview:")
        print(df.head())
    else:
        print("[ERROR] No data returned.")
