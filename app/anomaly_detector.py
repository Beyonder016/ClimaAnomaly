# anomaly_detector.py

import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, feature_cols=None, contamination=0.05):
    """Robust anomaly detection with imputation.

    * Cleans -999 / inf, coerces to numeric.
    * Uses Z‑score + IsolationForest in a Pipeline (Imputer → Scaler → IF).
    * Skips IF when <10 valid samples.
    """
    if feature_cols is None:
        feature_cols = [c for c in df.columns if c != "DATE"]

    # 1️⃣ Basic cleaning & coercion
    clean = (
        df.replace([-999, np.inf, -np.inf], np.nan)
          .assign(**{c: pd.to_numeric(df[c], errors="coerce") for c in feature_cols})
    )

    # 2️⃣ Z-score flags (row‑wise NaNs tolerated)
    z_cols = []
    for col in feature_cols:
        if clean[col].notna().sum() >= 5:  # need at least 5 pts for stats
            z = (clean[col] - clean[col].mean()) / clean[col].std(ddof=0)
            z_flag = (z.abs() > 3).astype(int)
            clean[f"z_{col}_anomaly"] = z_flag
            z_cols.append(f"z_{col}_anomaly")
        else:
            clean[f"z_{col}_anomaly"] = 0

    # 3️⃣ IsolationForest pipeline
    valid_rows = clean[feature_cols].dropna()
    clean["iforest_anomaly"] = 0  # default

    if len(valid_rows) >= 10:
        pipe = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            IsolationForest(
                n_estimators=100,
                contamination=contamination,
                random_state=42,
            ),
        )
        labels = pipe.fit_predict(valid_rows)
        iso_flags = pd.Series(labels == -1, index=valid_rows.index).astype(int)
        clean.loc[iso_flags.index, "iforest_anomaly"] = iso_flags

    # 4️⃣ Combined flag
    anom_cols = z_cols + ["iforest_anomaly"]
    clean["combined_anomaly"] = clean[anom_cols].sum(axis=1)
    clean["anomaly_flag"] = (clean["combined_anomaly"] > 0).astype(int)

    return clean


# Quick test
if __name__ == "__main__":
    from app.data_collector import fetch_climate_data

    df_sample = fetch_climate_data(28.6139, 77.2090, "20240101", "20241231")
    print(detect_anomalies(df_sample, ["T2M"]).head())
