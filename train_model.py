# ============================================================
#   ML MODEL TRAINER
#   Trains a Random Forest classifier on synthetic CBC data.
#
#   FIX (Bug 3): Removed StandardScaler from the Pipeline.
#     Random Forest is a tree-based model — completely invariant
#     to monotonic feature transformations. The scaler added zero
#     predictive value and only wasted memory + computation.
#
#   FIX (Bug 4): Removed unused import GradientBoostingClassifier.
#
#   FIX (Bug 5): confusion_matrix was imported but never used.
#     Now printed, showing which diseases confuse each other.
# ============================================================

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from generate_dataset import generate_dataset, GENERATORS

def train():
    print("=" * 60)
    print("  SMART BLOOD REPORT ANALYZER — ML MODEL TRAINER")
    print("=" * 60)

    # ── 1. Generate dataset ───────────────────────────────────
    print(f"\n[1/5] Generating synthetic dataset ({400} samples per class)...")
    X, y = generate_dataset()
    print(f"      Total samples: {len(X)}")
    print(f"      Features: {X.shape[1]}")
    print(f"      Classes: {y.nunique()}")

    # ── 2. Encode labels ──────────────────────────────────────
    from sklearn.preprocessing import LabelEncoder
    encoder = LabelEncoder()
    y_enc   = encoder.fit_transform(y)
    print(f"\n[2/5] Label encoding complete.")
    print(f"      Classes: {list(encoder.classes_)}")

    # ── 3. Train/test split ───────────────────────────────────
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )
    print(f"\n[3/5] Train/test split:")
    print(f"      Train: {len(X_train)} samples")
    print(f"      Test:  {len(X_test)}  samples")

    # ── 4. Train Random Forest ────────────────────────────────
    # NOTE: No StandardScaler — Random Forest is tree-based and
    # is invariant to feature scaling. Scaler was removed (Bug 3).
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    print(f"\n[4/5] Training Random Forest Classifier...")
    model.fit(X_train, y_train)
    print(f"      Training complete!")

    # ── 5. Evaluate ───────────────────────────────────────────
    from sklearn.metrics import (
        accuracy_score, f1_score, classification_report, confusion_matrix
    )
    from sklearn.model_selection import cross_val_score

    y_pred    = model.predict(X_test)
    accuracy  = round(accuracy_score(y_test, y_pred) * 100, 2)
    f1        = round(f1_score(y_test, y_pred, average="weighted") * 100, 2)

    cv_scores = cross_val_score(model, X, y_enc, cv=5, scoring="accuracy", n_jobs=-1)
    cv_mean   = round(cv_scores.mean() * 100, 2)
    cv_std    = round(cv_scores.std()  * 100, 2)

    print(f"\n[5/5] Evaluating model...")
    print()
    print("─" * 60)
    print(f"  TEST ACCURACY  : {accuracy}%")
    print(f"  WEIGHTED F1    : {f1}%")
    print("─" * 60)
    print()
    print(f"  5-FOLD CROSS-VALIDATION:")
    print(f"  Scores : {[f'{s*100:.1f}%' for s in cv_scores]}")
    print(f"  Mean   : {cv_mean}%  ±  {cv_std}%")
    print()

    # Per-class report
    print(f"  PER-CLASS CLASSIFICATION REPORT:")
    print("─" * 60)
    print(classification_report(
        y_test, y_pred,
        target_names=encoder.classes_,
        digits=3
    ))

    # FIX Bug 5: Confusion matrix now actually printed
    print(f"\n  CONFUSION MATRIX:")
    print("─" * 60)
    cm     = confusion_matrix(y_test, y_pred)
    labels = [c[:6] + ".." if len(c) > 8 else c for c in encoder.classes_]
    header = "  {:>35s}  " + "  {:>7s}" * len(labels)
    print(header.format("", *[l[:7] for l in labels]))
    for i, row in enumerate(cm):
        row_str = "  {:>35s}  " + "  {:>7d}" * len(row)
        print(row_str.format(encoder.classes_[i][:35], *row))

    # Feature importances
    print(f"\n  TOP FEATURE IMPORTANCES:")
    print("─" * 60)
    importances = model.feature_importances_
    feat_names  = list(X.columns)
    feat_sorted = sorted(zip(feat_names, importances), key=lambda x: x[1], reverse=True)
    for feat, imp in feat_sorted:
        bar = "█" * int(imp * 70)
        print(f"  {feat:<18}{bar:<30}{imp*100:.2f}%")

    # ── 6. Save model ─────────────────────────────────────────
    import joblib
    model_data = {
        "model":    model,
        "encoder":  encoder,
        "features": feat_names,
        "accuracy": accuracy,
        "f1_score": f1,
        "cv_mean":  cv_mean,
        "cv_std":   cv_std,
    }
    model_path = os.path.join(os.path.dirname(__file__), "ml_model.pkl")
    joblib.dump(model_data, model_path)
    size_kb = os.path.getsize(model_path) / 1024
    print(f"\n  ✅ Model saved to: ml_model.pkl")
    print(f"  File size: {size_kb:.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    train()
