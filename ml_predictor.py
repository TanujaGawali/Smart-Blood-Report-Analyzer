# ============================================================
#   ML PREDICTOR
#   Loads trained Random Forest model and predicts diseases
#   from CBC values with confidence scores.
#
#   FIX (Bug 1): Replaced _model_cache = None with a sentinel
#   object so failed loads are never cached — model retries on
#   next call instead of returning None permanently.
# ============================================================

import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_model.pkl")

FEATURES = [
    "Hemoglobin", "PCV", "RBC", "WBC", "Platelets",
    "MCV", "MCH", "MCHC", "RDW",
    "Neutrophils", "Lymphocytes", "Eosinophils", "Monocytes", "Basophils",
]

# Default fill values (mid-range normals) used when a feature is missing from input
DEFAULTS = {
    "Hemoglobin":  15.0,
    "PCV":         45.0,
    "RBC":         5.0,
    "WBC":         7000,
    "Platelets":   280000,
    "MCV":         90.0,
    "MCH":         30.0,
    "MCHC":        33.5,
    "RDW":         13.0,
    "Neutrophils": 57.0,
    "Lymphocytes": 30.0,
    "Eosinophils": 2.5,
    "Monocytes":   5.0,
    "Basophils":   0.5,
}

# Sentinel — distinguishes "not yet loaded" from "loaded and is None"
_NOT_LOADED = object()
_model_cache = _NOT_LOADED


def load_model():
    """
    Load model from disk (cached after first SUCCESSFUL load).
    Returns model dict or None if unavailable.

    FIX: Uses sentinel pattern so a failed load is never cached.
    The old code cached None on failure so the model was never retried.
    """
    global _model_cache
    if _model_cache is _NOT_LOADED:
        try:
            import joblib
            loaded = joblib.load(MODEL_PATH)
            _model_cache = loaded          # cache only on success
            print(f"[ml_predictor] Model loaded: {MODEL_PATH}")
        except Exception as e:
            print(f"[ml_predictor] ⚠️ Could not load ML model: {e}")
            return None                    # do NOT cache failure
    return _model_cache


def ml_predict(values: dict, top_n: int = 3):
    """
    Predict diseases from CBC values using the trained Random Forest model.

    Args:
        values: dict of {parameter_name: float_value}
        top_n:  number of top predictions to return

    Returns:
        List of (disease_name, confidence_percent) tuples,
        sorted by confidence descending.
        Returns empty list if model not available.
    """
    model_data = load_model()
    if model_data is None:
        return []

    model   = model_data["model"]
    encoder = model_data["encoder"]

    # Build feature vector as DataFrame so sklearn doesn't warn about feature names
    import pandas as pd
    feature_vector = pd.DataFrame(
        [[values.get(f, DEFAULTS[f]) for f in FEATURES]],
        columns=FEATURES
    )

    # Get probability distribution across all classes
    proba = model.predict_proba(feature_vector)[0]

    # Map class probabilities to disease names
    class_probs = [
        (encoder.classes_[i], round(prob * 100, 1))
        for i, prob in enumerate(proba)
    ]

    # Sort by confidence descending
    class_probs.sort(key=lambda x: x[1], reverse=True)

    # Only return predictions with meaningful confidence (≥10%)
    results = [(name, conf) for name, conf in class_probs if conf >= 10.0]

    return results[:top_n]


def ml_model_info():
    """Return model metadata for the UI badge."""
    model_data = load_model()
    if model_data is None:
        return None
    return {
        "accuracy": model_data.get("accuracy", "N/A"),
        "f1_score": model_data.get("f1_score", "N/A"),
        "cv_mean":  model_data.get("cv_mean",  "N/A"),
    }


if __name__ == "__main__":
    # Quick smoke-test with Yash's CBC values
    test_values = {
        "Hemoglobin":  12.5,
        "PCV":         57.5,
        "WBC":         9000,
        "RBC":         5.2,
        "Platelets":   150000,
        "MCV":         87.75,
        "MCH":         27.2,
        "MCHC":        32.8,
        "RDW":         13.6,
        "Neutrophils": 60,
        "Lymphocytes": 31,
        "Eosinophils": 1,
        "Monocytes":   7,
        "Basophils":   1,
    }
    print("Testing ML predictor with Yash's CBC values...")
    for disease, conf in ml_predict(test_values):
        print(f"  {conf:>6.1f}%  →  {disease}")
    info = ml_model_info()
    if info:
        print(f"\nModel: Accuracy={info['accuracy']}%  F1={info['f1_score']}%  CV={info['cv_mean']}%")
