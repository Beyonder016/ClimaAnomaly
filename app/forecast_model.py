# forecast_model.py

import pandas as pd
from prophet import Prophet
import os

models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

def forecast_climate_metric(df, metric="T2M", forecast_days=30, save_model=True):
    """
    Forecast future climate values using Prophet.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'DATE' and metric column
        metric (str): The metric to forecast (e.g., 'T2M')
        forecast_days (int): Number of days to forecast
        save_model (bool): If True, saves the model to /models/

    Returns:
        forecast_df (pd.DataFrame): DataFrame with forecast and confidence intervals
    """
    df_prophet = df[['DATE', metric]].rename(columns={"DATE": "ds", metric: "y"})

    model = Prophet(daily_seasonality=True)
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    if save_model:
        model_path = os.path.join(models_dir, f"prophet_{metric}.pkl")
        try:
            import joblib
            joblib.dump(model, model_path)
            print(f"[INFO] Model saved: {model_path}")
        except Exception as e:
            print("[WARNING] Could not save model:", e)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Example usage
if __name__ == "__main__":
    from app.data_collector import fetch_climate_data

    df = fetch_climate_data(
        lat=18.5204,
        lon=73.8567,
        start_date="20230101",
        end_date="20231231"
    )

    forecast_df = forecast_climate_metric(df, metric="T2M")
    print(forecast_df.tail())
