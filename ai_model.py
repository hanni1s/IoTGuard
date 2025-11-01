import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import os

_model = None
MODEL_PATH = "ai_risk_model.pkl"

def train_ai_model(data):
    """
    Train the AI risk prediction model based on past scans.
    'data' should be a list of dictionaries (each with 'Port' and 'Risk Level')
    """
    global _model

    df = pd.DataFrame(data)

    # Basic validation
    if df.empty or "Risk Level" not in df.columns or len(df) < 5:
        print("[AI Model] Not enough data to train.")
        return None

    # Encode risk levels
    encoder = LabelEncoder()
    df["Encoded Risk"] = encoder.fit_transform(df["Risk Level"])

    # Normalize ports to handle extreme ranges
    df["Port_Normalized"] = df["Port"].apply(lambda x: x / 65535)

    X = df[["Port_Normalized"]]
    y = df["Encoded Risk"]

    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(X, y)
    _model = (model, encoder)

    # Save model to file (persistent learning)
    joblib.dump(_model, MODEL_PATH)

    print("[AI Model] Training complete. Model saved.")
    return model


def load_ai_model():
    """Load trained model from file if available."""
    global _model
    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
        print("[AI Model] Loaded existing model.")
        return _model
    return None


def predict_overall_risk(scan_results):
    """
    Predict overall IoT device risk level based on open ports.
    """
    global _model

    if not scan_results:
        return "Unknown"

    # Load or train model if not ready
    if _model is None:
        load_ai_model()
        if _model is None:
            train_ai_model(scan_results)

    model, encoder = _model

    ports = pd.DataFrame([r["Port"] for r in scan_results], columns=["Port"])
    ports["Port_Normalized"] = ports["Port"].apply(lambda x: x / 65535)

    predictions = model.predict(ports[["Port_Normalized"]])
    decoded_preds = encoder.inverse_transform(predictions)

    # Weighted scoring (slightly smarter logic)
    score = 0
    for risk in decoded_preds:
        if "High" in risk:
            score += 3
        elif "Medium" in risk:
            score += 2
        else:
            score += 1

    avg_score = score / len(decoded_preds)

    if avg_score >= 2.5:
        return "High Risk"
    elif avg_score >= 1.7:
        return "Medium Risk"
    else:
        return "Low Risk"