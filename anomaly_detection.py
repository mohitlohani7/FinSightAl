import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state
        )
        self.is_fitted = False

    def fit(self, X: pd.DataFrame):
        if X.empty:
            raise ValueError("Input data is empty.")
        self.model.fit(X)
        self.is_fitted = True

    def detect(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before detection.")
        labels = self.model.predict(X)  # -1 anomaly, 1 normal
        X_out = X.copy()
        X_out["Anomaly"] = (labels == -1)
        return X_out


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    # Check if 'Amount' exists
    if 'Amount' not in df.columns:
        raise KeyError("Column 'Amount' is missing from the dataset!")

    # Select numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns found for anomaly detection.")

    # Drop rows with NA in numeric cols
    data = df[numeric_cols].dropna()
    if data.empty:
        raise ValueError("No valid numeric data available after dropping NA.")

    # Initialize and fit model
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(data)

    # Predict anomalies
    preds = model.predict(data)

    # Add is_anomaly flag to original df indexed by data.index
    df_anom = df.loc[data.index].copy()
    df_anom['is_anomaly'] = preds == -1

    return df_anom
