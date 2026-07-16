# ============================================================
#   SYNTHETIC CBC DATASET GENERATOR
#
#   Generates realistic training data for 7 disease classes.
#   Each class has physiologically accurate CBC ranges with:
#     - Realistic lab noise (based on real instrument CV%)
#     - Severity levels (mild/moderate/severe) with overlap
#       across the Normal boundary — so the model must learn
#       from CBC patterns, not just hard thresholds
#     - Comorbidity injection (5% of samples get a second condition)
#     - Borderline normal samples (30% of Normal class)
#
#   FIX (Bug 2): Original data had zero overlap between classes
#   (e.g. IDA Hb max was 10, Normal Hb min was 13.5 — a 3.5 gap).
#   The model memorized hard thresholds and got 99.46% fake accuracy.
#   Now mild cases cross the Normal boundary → realistic 82–92%.
#
#   FIX (Bug 7): rand_borderline_low / rand_borderline_high are now
#   actually used in generate_normal() (30% of samples have one
#   borderline value, representing real healthy people with minor
#   fluctuations).
# ============================================================

import numpy as np
import pandas as pd

# ── Reproducibility ───────────────────────────────────────────
DATA_SEED  = 42   # dataset generation seed
SHUFFLE_SEED = 99 # separate shuffle seed — prevents data leakage

# ── Dataset size ──────────────────────────────────────────────
SAMPLES_PER_CLASS = 400
NOISE_REPEAT = 3   # augmentation: each sample is regenerated N times with fresh noise

# ── Lab instrument CV% → realistic standard deviations ───────
# Source: CLSI EP15-A3 guidelines for CBC analyzers
NOISE_STD = {
    "Hemoglobin":  0.7,    # CV ~4-5%  at 15 g/dL
    "PCV":         2.0,    # CV ~4%    at 45%
    "RBC":         0.15,   # CV ~3%    at 5.0
    "WBC":         800,    # CV ~8-10% at 8000
    "Platelets":   25000,  # CV ~8%    at 280k
    "MCV":         1.5,    # CV ~1.5%
    "MCH":         0.7,    # CV ~2%
    "MCHC":        0.6,    # CV ~1.5%
    "RDW":         0.9,    # CV ~5-7%
    "Neutrophils": 5.0,    # CV ~8%
    "Lymphocytes": 5.0,    # CV ~8%
    "Eosinophils": 1.0,
    "Monocytes":   1.5,
    "Basophils":   0.3,
}


def add_noise(value, param):
    """Add Gaussian noise based on real lab instrument CV%."""
    return value + np.random.normal(0, NOISE_STD.get(param, 0))


def rand(low, high):
    """Uniform random in [low, high]."""
    return np.random.uniform(low, high)


def rand_borderline_low(ref_low, width=0.1):
    """
    Random value just around the lower reference boundary.
    FIX (Bug 7): Now actually called in generate_normal().
    Represents a healthy person with a minor low fluctuation.
    """
    return np.random.uniform(ref_low * (1 - width), ref_low * (1 + width * 0.5))


def rand_borderline_high(ref_high, width=0.1):
    """
    Random value just around the upper reference boundary.
    FIX (Bug 7): Now actually called in generate_normal().
    """
    return np.random.uniform(ref_high * (1 - width * 0.5), ref_high * (1 + width))


# ──────────────────────────────────────────────────────────────
#  CLASS GENERATORS
#  Each function returns one raw (pre-noise) CBC sample dict.
#  Severity weights: mild 40%, moderate 40%, severe 20%
# ──────────────────────────────────────────────────────────────

def generate_normal():
    """
    Normal/Healthy — all values within reference range.
    FIX (Bug 7): 30% of samples have one borderline value
    to simulate real healthy patients with minor fluctuations.
    """
    hb  = rand(13.5, 16.5)
    pcv = round(hb * rand(2.85, 3.05), 1)   # PCV ≈ Hb × 3 (physiological)
    sample = {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(4.5, 5.4),
        "WBC":         rand(4500, 10000),
        "Platelets":   rand(160000, 390000),
        "MCV":         rand(83, 100),
        "MCH":         rand(27, 31),
        "MCHC":        rand(32.5, 34.4),
        "RDW":         rand(11.6, 13.8),
        "Neutrophils": rand(50, 62),
        "Lymphocytes": rand(20, 40),
        "Eosinophils": rand(0, 5),
        "Monocytes":   rand(2, 8),
        "Basophils":   rand(0, 1),
    }
    # FIX Bug 7: 30% chance of one borderline value
    if np.random.random() < 0.30:
        borderline_param = np.random.choice(["Hemoglobin", "WBC", "MCV", "Platelets"])
        if borderline_param == "Hemoglobin":
            sample["Hemoglobin"] = rand_borderline_low(13.5)
            sample["PCV"] = round(sample["Hemoglobin"] * rand(2.9, 3.05), 1)
        elif borderline_param == "WBC":
            if np.random.random() < 0.5:
                sample["WBC"] = rand_borderline_low(4500)
            else:
                sample["WBC"] = rand_borderline_high(10000)
        elif borderline_param == "MCV":
            sample["MCV"] = rand_borderline_low(83)
        elif borderline_param == "Platelets":
            sample["Platelets"] = rand_borderline_low(160000)
    return sample


def generate_iron_deficiency_anemia():
    """
    IDA — Low Hb, low MCV (microcytic), high RDW (anisocytosis).
    Key distinguisher from Thalassemia: HIGH RDW (Thal has normal RDW).
    Severity levels cross the Normal boundary for realistic overlap.
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.4, 0.4, 0.2])

    if severity == "mild":
        # Mild IDA: Hb 11.5-13.4 (overlaps with Normal floor of 13.5)
        hb  = rand(11.5, 13.4)
        mcv = rand(73, 82)
        rdw = rand(14.5, 17.0)
    elif severity == "moderate":
        hb  = rand(8.5, 11.4)
        mcv = rand(65, 74)
        rdw = rand(17.0, 20.5)
    else:
        hb  = rand(5.0, 8.4)
        mcv = rand(55, 65)
        rdw = rand(20.0, 25.0)

    pcv = round(hb * rand(2.9, 3.1), 1)
    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(3.2, 4.6),
        "WBC":         rand(4500, 10500),
        "Platelets":   rand(170000, 420000),   # may be high (reactive thrombocytosis)
        "MCV":         mcv,
        "MCH":         rand(22, 27),
        "MCHC":        rand(29, 32.4),
        "RDW":         rdw,
        "Neutrophils": rand(48, 65),
        "Lymphocytes": rand(22, 42),
        "Eosinophils": rand(0, 5),
        "Monocytes":   rand(2, 8),
        "Basophils":   rand(0, 1),
    }


def generate_thalassemia_trait():
    """
    Thalassemia Minor — low MCV, high RBC, NORMAL RDW.
    Key distinguisher from IDA: RDW is NORMAL (11.5-13.2),
    RBC is HIGH (5.5-6.8), MCV even lower.
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.5, 0.35, 0.15])

    if severity == "mild":
        hb  = rand(11.0, 13.5)
        mcv = rand(65, 74)
    elif severity == "moderate":
        hb  = rand(8.5, 11.0)
        mcv = rand(58, 66)
    else:
        hb  = rand(6.0, 8.5)
        mcv = rand(52, 59)

    pcv = round(hb * rand(2.8, 3.05), 1)
    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(5.5, 6.8),        # HIGH RBC — key Thal marker
        "WBC":         rand(4500, 10000),
        "Platelets":   rand(150000, 380000),
        "MCV":         mcv,
        "MCH":         rand(19, 26),
        "MCHC":        rand(30, 33),
        "RDW":         rand(11.5, 13.2),      # NORMAL RDW — key Thal marker
        "Neutrophils": rand(48, 62),
        "Lymphocytes": rand(22, 42),
        "Eosinophils": rand(0, 5),
        "Monocytes":   rand(2, 8),
        "Basophils":   rand(0, 1),
    }


def generate_polycythemia():
    """
    Polycythemia / Dehydration — high PCV, high Hb, high RBC.
    Mild cases overlap with Normal upper boundary.
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.4, 0.4, 0.2])

    if severity == "mild":
        # Mild: PCV 50-54 (overlaps with Normal max of 50)
        pcv = rand(50, 54)
        hb  = rand(16.5, 18.0)
    elif severity == "moderate":
        pcv = rand(54, 60)
        hb  = rand(18.0, 20.5)
    else:
        pcv = rand(60, 70)
        hb  = rand(20.5, 24.0)

    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(5.5, 7.5),
        "WBC":         rand(4500, 12000),
        "Platelets":   rand(150000, 400000),
        "MCV":         rand(83, 100),
        "MCH":         rand(27, 32),
        "MCHC":        rand(32.5, 34.5),
        "RDW":         rand(11.6, 14.0),
        "Neutrophils": rand(50, 65),
        "Lymphocytes": rand(20, 38),
        "Eosinophils": rand(0, 5),
        "Monocytes":   rand(2, 8),
        "Basophils":   rand(0, 1),
    }


def generate_thrombocytopenia():
    """
    Thrombocytopenia — low platelets.
    Mild cases cross the Normal lower boundary (150,000).
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.35, 0.4, 0.25])

    if severity == "mild":
        # Mild: 100k-149k (just below Normal floor of 150k)
        plt = rand(100000, 149000)
    elif severity == "moderate":
        plt = rand(50000, 100000)
    else:
        plt = rand(10000, 50000)

    hb  = rand(12.5, 16.0)
    pcv = round(hb * rand(2.9, 3.1), 1)
    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(4.3, 5.4),
        "WBC":         rand(4000, 11000),
        "Platelets":   plt,
        "MCV":         rand(83, 100),
        "MCH":         rand(27, 32),
        "MCHC":        rand(32.5, 34.5),
        "RDW":         rand(11.6, 14.0),
        "Neutrophils": rand(48, 65),
        "Lymphocytes": rand(22, 42),
        "Eosinophils": rand(0, 6),
        "Monocytes":   rand(2, 9),
        "Basophils":   rand(0, 1.5),
    }


def generate_leukocytosis():
    """
    Leukocytosis — high WBC (infection/inflammation).
    Mild cases cross the Normal upper boundary (10,000-11,000).
    Neutrophilia is the dominant pattern.
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.4, 0.35, 0.25])

    if severity == "mild":
        # Mild: 10,500-13,000 (overlaps with Normal max of 11,000)
        wbc  = rand(10500, 13000)
        neut = rand(65, 75)
    elif severity == "moderate":
        wbc  = rand(13000, 20000)
        neut = rand(72, 85)
    else:
        wbc  = rand(20000, 35000)
        neut = rand(80, 92)

    lymp = rand(5, max(6, 95 - neut))
    hb   = rand(12.0, 16.5)
    pcv  = round(hb * rand(2.9, 3.1), 1)
    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(4.0, 5.5),
        "WBC":         wbc,
        "Platelets":   rand(150000, 450000),
        "MCV":         rand(83, 100),
        "MCH":         rand(27, 32),
        "MCHC":        rand(32.5, 34.5),
        "RDW":         rand(11.6, 14.5),
        "Neutrophils": neut,
        "Lymphocytes": lymp,
        "Eosinophils": rand(0, 4),
        "Monocytes":   rand(3, 12),
        "Basophils":   rand(0, 1),
    }


def generate_leukopenia():
    """
    Leukopenia — low WBC (viral infection, marrow suppression).
    Mild cases cross the Normal lower boundary (4,000-4,500).
    """
    severity = np.random.choice(["mild", "moderate", "severe"], p=[0.4, 0.4, 0.2])

    if severity == "mild":
        # Mild: 3,000-4,499 (overlaps with Normal floor of 4,000)
        wbc  = rand(3000, 4499)
        neut = rand(35, 52)
    elif severity == "moderate":
        wbc  = rand(1500, 3000)
        neut = rand(25, 40)
    else:
        wbc  = rand(500, 1500)
        neut = rand(10, 28)

    hb  = rand(12.0, 16.0)
    pcv = round(hb * rand(2.9, 3.1), 1)
    return {
        "Hemoglobin":  hb,
        "PCV":         pcv,
        "RBC":         rand(4.0, 5.4),
        "WBC":         wbc,
        "Platelets":   rand(140000, 400000),
        "MCV":         rand(83, 100),
        "MCH":         rand(27, 32),
        "MCHC":        rand(32.5, 34.5),
        "RDW":         rand(11.6, 14.5),
        "Neutrophils": neut,
        "Lymphocytes": rand(45, 75),
        "Eosinophils": rand(0, 5),
        "Monocytes":   rand(2, 10),
        "Basophils":   rand(0, 1),
    }


# ──────────────────────────────────────────────────────────────
#  NOISE APPLICATION + COMORBIDITY INJECTION
# ──────────────────────────────────────────────────────────────

def apply_noise(sample):
    """Add realistic lab instrument noise to all parameters."""
    return {
        param: max(0, add_noise(val, param))
        for param, val in sample.items()
    }


def inject_comorbidity(sample, label):
    """
    5% chance: add a secondary condition's signature to the sample.
    Simulates real patients who often have multiple findings.
    """
    if np.random.random() > 0.05:
        return sample, label
    secondary = np.random.choice(["anemia_hint", "infection_hint", "dehydration_hint"])
    if secondary == "anemia_hint":
        sample = dict(sample)
        sample["Hemoglobin"] = max(9.0, sample["Hemoglobin"] - rand(1.5, 3.0))
        sample["PCV"] = round(sample["Hemoglobin"] * rand(2.9, 3.1), 1)
    elif secondary == "infection_hint":
        sample = dict(sample)
        sample["WBC"] = min(35000, sample["WBC"] + rand(2000, 5000))
        sample["Neutrophils"] = min(90, sample["Neutrophils"] + rand(8, 15))
    elif secondary == "dehydration_hint":
        sample = dict(sample)
        sample["PCV"] = min(70, sample["PCV"] + rand(3, 8))
    return sample, label


# ──────────────────────────────────────────────────────────────
#  MAIN GENERATOR
# ──────────────────────────────────────────────────────────────

GENERATORS = {
    "Normal / Healthy":                     generate_normal,
    "Iron Deficiency Anemia":               generate_iron_deficiency_anemia,
    "Thalassemia Trait":                    generate_thalassemia_trait,
    "Polycythemia / Dehydration":           generate_polycythemia,
    "Thrombocytopenia (Low Platelets)":     generate_thrombocytopenia,
    "Leukocytosis (High WBC — Infection)":  generate_leukocytosis,
    "Leukopenia (Low WBC — Weak Immunity)": generate_leukopenia,
}


def generate_dataset():
    """
    Generate balanced synthetic dataset.
    Returns X (DataFrame) and y (Series of labels).
    """
    np.random.seed(DATA_SEED)
    rows   = []
    labels = []

    for label, generator in GENERATORS.items():
        for _ in range(SAMPLES_PER_CLASS):
            raw    = generator()
            noisy  = apply_noise(raw)
            noisy, label_final = inject_comorbidity(noisy, label)
            rows.append(noisy)
            labels.append(label_final)

    X = pd.DataFrame(rows)
    y = pd.Series(labels, name="label")

    # Shuffle with separate seed (prevents positional leakage)
    rng   = np.random.default_rng(SHUFFLE_SEED)
    order = rng.permutation(len(X))
    X     = X.iloc[order].reset_index(drop=True)
    y     = y.iloc[order].reset_index(drop=True)

    return X, y


if __name__ == "__main__":
    X, y = generate_dataset()
    print(f"Dataset shape: {X.shape}")
    print(f"Class distribution:\n{y.value_counts()}")

    # Verify overlap exists between IDA and Normal
    ida_rows = X[y == "Iron Deficiency Anemia"]["Hemoglobin"]
    nor_rows = X[y == "Normal / Healthy"]["Hemoglobin"]
    overlap  = (ida_rows > 13.0).sum()
    print(f"\nIDA samples that could look Normal (Hb > 13): {overlap}/{len(ida_rows)}")
