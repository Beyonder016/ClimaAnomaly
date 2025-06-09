from app.data_collector import fetch_climate_data

df = fetch_climate_data(
    lat=28.6139,
    lon=77.2090,
    start_date="20230101",
    end_date="20231231"
)

if df is not None:
    print("[✅] Data fetched successfully:")
    print(df.head())
else:
    print("[❌] No data returned.")
