# ============================================================
#   ANALYZER ENGINE
#   - Abnormality Detection
#   - Disease Prediction
#   - Health Score Calculation
# ============================================================

from disease_db import REFERENCE_RANGES, DISEASE_DB

# Try to import ML predictor — fall back gracefully if model not found
try:
    from ml_predictor import ml_predict, ml_model_info
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False


# ──────────────────────────────────────────────
#  1. ABNORMALITY DETECTION
# ──────────────────────────────────────────────

def detect_abnormalities(values, age_group="Male"):
    """
    Compare extracted CBC values against reference ranges.
    Returns list of dicts with status for each parameter.
    """
    results = []

    for param, value in values.items():
        if param not in REFERENCE_RANGES:
            continue

        ref = REFERENCE_RANGES[param].get(age_group, REFERENCE_RANGES[param]["Male"])
        low  = ref["low"]
        high = ref["high"]
        unit = ref["unit"]

        # Determine status
        if value < low:
            deviation = ((low - value) / low) * 100
            if deviation > 30:
                status = "Critical Low"
                color  = "🔴"
            elif deviation > 15:
                status = "Low"
                color  = "🔴"
            else:
                status = "Borderline Low"
                color  = "🟡"
        elif value > high:
            deviation = ((value - high) / high) * 100
            if deviation > 30:
                status = "Critical High"
                color  = "🟠"
            elif deviation > 15:
                status = "High"
                color  = "🟠"
            else:
                status = "Borderline High"
                color  = "🟡"
        else:
            status = "Normal"
            color  = "🟢"
            deviation = 0

        results.append({
            "parameter": param,
            "value":     value,
            "unit":      unit,
            "low":       low,
            "high":      high,
            "status":    status,
            "color":     color,
            "deviation": round(deviation, 1) if status != "Normal" else 0,
        })

    return results


# ──────────────────────────────────────────────
#  2. DISEASE PREDICTION ENGINE
# ──────────────────────────────────────────────

def predict_diseases(values, age_group="Male"):
    """
    Rule-based disease prediction from CBC pattern matching.
    Returns list of (disease_name, confidence_percent) tuples.
    """
    predictions = []

    hb   = values.get("Hemoglobin")
    pcv  = values.get("PCV")
    wbc  = values.get("WBC")
    plt  = values.get("Platelets")
    mcv  = values.get("MCV")
    mch  = values.get("MCH")
    mchc = values.get("MCHC")
    rdw  = values.get("RDW")
    neu  = values.get("Neutrophils")
    lym  = values.get("Lymphocytes")
    eos  = values.get("Eosinophils")

    ref_hb  = REFERENCE_RANGES["Hemoglobin"].get(age_group, REFERENCE_RANGES["Hemoglobin"]["Male"])
    ref_pcv = REFERENCE_RANGES["PCV"].get(age_group, REFERENCE_RANGES["PCV"]["Male"])
    ref_wbc = REFERENCE_RANGES["WBC"]["Male"]
    ref_plt = REFERENCE_RANGES["Platelets"]["Male"]

    # ── Iron Deficiency Anemia ──────────────────
    score = 0
    if hb  and hb  < ref_hb["low"]:  score += 40
    if mcv and mcv < 83:              score += 20
    if mch and mch < 27:              score += 20
    if rdw and rdw > 14:              score += 20
    if score >= 40:
        predictions.append(("Iron Deficiency Anemia", min(score, 95)))

    # ── Polycythemia / Dehydration ──────────────
    score = 0
    if pcv and pcv > ref_pcv["high"]: score += 60
    if hb  and hb  > ref_hb["high"]: score += 30
    if score >= 60:
        predictions.append(("Polycythemia / Dehydration", min(score, 92)))

    # ── Thrombocytopenia (Low Platelets) ────────
    score = 0
    if plt:
        if plt < 100000:  score = 90
        elif plt < 150000: score = 70
        elif plt <= 155000: score = 45   # borderline
    if score >= 50:
        predictions.append(("Thrombocytopenia (Low Platelets)", score))

    # ── Leukocytosis (High WBC) ─────────────────
    score = 0
    if wbc:
        if wbc > 15000:   score = 85
        elif wbc > 11000: score = 65
        if neu and neu > 70: score += 10
    if score >= 65:
        predictions.append(("Leukocytosis (High WBC — Infection)", min(score, 92)))

    # ── Leukopenia (Low WBC) ────────────────────
    score = 0
    if wbc and wbc < ref_wbc["low"]:
        dev = ((ref_wbc["low"] - wbc) / ref_wbc["low"]) * 100
        score = min(int(50 + dev), 90)
    if score >= 50:
        predictions.append(("Leukopenia (Low WBC — Weak Immunity)", score))

    # ── Thalassemia Trait ───────────────────────
    score = 0
    if hb  and hb  < ref_hb["low"]: score += 30
    if mcv and mcv < 75:             score += 40
    if rdw and rdw < 14:             score += 20   # RDW normal in thalassemia
    if mchc and mchc < 32:           score += 10
    if score >= 60:
        predictions.append(("Thalassemia Trait", min(score, 80)))

    # Sort by confidence descending
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions


# ──────────────────────────────────────────────
#  3. HEALTH SCORE CALCULATOR
# ──────────────────────────────────────────────

def calculate_health_score(abnormalities):
    """
    Calculate overall health score (0–100) based on abnormal parameters.
    """
    if not abnormalities:
        return 100, "Excellent", "All parameters are within normal range!"

    total_params = len(abnormalities)
    penalty = 0

    status_penalty = {
        "Normal":          0,
        "Borderline Low":  12,
        "Borderline High": 12,
        "Low":             22,
        "High":            22,
        "Critical Low":    35,
        "Critical High":   35,
    }

    for item in abnormalities:
        penalty += status_penalty.get(item["status"], 0)

    score = max(0, 100 - penalty)

    if score >= 90:
        label  = "Excellent 🌟"
        advice = "All parameters are healthy. Routine checkup in 1 year."
    elif score >= 75:
        label  = "Good ✅"
        advice = "Minor concerns detected. Monitor and retest in 3 months."
    elif score >= 60:
        label  = "Moderate ⚠️"
        advice = "Some abnormal values detected. Consult a doctor within 1 week."
    elif score >= 40:
        label  = "Poor 🔶"
        advice = "Multiple abnormal values. Please see a doctor within 2 days."
    else:
        label  = "Critical 🚨"
        advice = "Critically abnormal values detected. Visit emergency immediately!"

    return score, label, advice


# ──────────────────────────────────────────────
#  4. FULL ANALYSIS PIPELINE
# ──────────────────────────────────────────────

def run_full_analysis(values, age_group="Male"):
    """
    Run complete analysis pipeline.
    Uses ML model if available, else falls back to rule-based.
    Returns dict with all results.
    """
    abnormalities = detect_abnormalities(values, age_group)
    score, label, advice = calculate_health_score(abnormalities)

    # ── Disease Prediction: ML first, rule-based fallback ────
    prediction_method = "rule-based"
    if ML_AVAILABLE:
        raw_predictions = ml_predict(values, top_n=3)

        # Build a quick lookup of which parameters are abnormal
        abnormal_params = {a["parameter"] for a in abnormalities if a["status"] != "Normal"}
        n_abnormal = len(abnormal_params)

        # Key parameters that MUST be abnormal for each disease to be shown.
        # If none of a disease's key params are abnormal, suppress it
        # regardless of ML confidence — the model is firing on noise.
        DISEASE_KEY_PARAMS = {
            "Iron Deficiency Anemia":               {"Hemoglobin", "MCV", "RDW", "MCH"},
            "Polycythemia / Dehydration":           {"PCV", "Hemoglobin", "RBC"},
            "Thrombocytopenia (Low Platelets)":     {"Platelets"},
            "Leukocytosis (High WBC — Infection)":  {"WBC", "Neutrophils"},
            "Leukopenia (Low WBC — Weak Immunity)": {"WBC", "Neutrophils"},
            "Thalassemia Trait":                    {"Hemoglobin", "MCV", "MCH", "RBC"},
        }

        non_normal = [(n, c) for n, c in raw_predictions if n != "Normal / Healthy"]
        top_disease_conf = non_normal[0][1] if non_normal else 0
        top_pred_name    = raw_predictions[0][0] if raw_predictions else "Normal / Healthy"

        # Rule 1: Model says clearly Normal/Healthy → no disease
        if top_pred_name == "Normal / Healthy" and raw_predictions[0][1] >= 50:
            diseases_raw = []
        # Rule 2: Top confidence too low regardless → suppress all
        elif top_disease_conf < 25:
            diseases_raw = []
        else:
            # Filter each predicted disease individually
            filtered = []
            for name, conf in non_normal:
                key_params = DISEASE_KEY_PARAMS.get(name, set())
                has_relevant_abnormal = bool(key_params & abnormal_params)

                # Keep disease only if:
                # - High confidence (≥40%) regardless of param check, OR
                # - Medium confidence (≥30%) AND has a relevant abnormal param, OR
                # - Any confidence AND multiple relevant params are abnormal
                relevant_abnormal_count = len(key_params & abnormal_params)
                if conf >= 40:
                    filtered.append((name, conf))
                elif conf >= 30 and has_relevant_abnormal:
                    filtered.append((name, conf))
                elif relevant_abnormal_count >= 2:
                    filtered.append((name, conf))
                # else: suppress — ML noise, not supported by actual CBC values

            diseases_raw = filtered
        prediction_method = "ml"
    else:
        diseases_raw = predict_diseases(values, age_group)

    # ── Build detailed disease info ───────────────────────────
    disease_details = []
    for disease_name, confidence in diseases_raw:
        detail = DISEASE_DB.get(disease_name, {})
        disease_details.append({
            "name":        disease_name,
            "confidence":  confidence,
            "description": detail.get("description", "No description available."),
            "urgency":     detail.get("urgency", "Consult your doctor."),
            "doctor":      detail.get("doctor_type", "General Physician"),
            "foods_eat":   detail.get("foods_eat", []),
            "foods_avoid": detail.get("foods_avoid", []),
            "medicines":   detail.get("medicines", []),
            "lifestyle":   detail.get("lifestyle", []),
            "severity":    detail.get("severity_info", {}),
        })

    # ── ML model metadata ─────────────────────────────────────
    ml_info = ml_model_info() if ML_AVAILABLE else None

    return {
        "abnormalities":       abnormalities,
        "diseases":            disease_details,
        "health_score":        score,
        "score_label":         label,
        "score_advice":        advice,
        "prediction_method":   prediction_method,
        "ml_info":             ml_info,
    }