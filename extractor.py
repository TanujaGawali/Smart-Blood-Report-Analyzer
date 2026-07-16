# ============================================================
#   PDF EXTRACTOR + CBC VALUE EXTRACTOR
#   Tested against: Flabs, Drlogy, SRN Diagnostics, Crystal Data Inc.
#
#   Extraction methods tried in order:
#   1. pdfplumber   — digital/text PDFs (fastest, most accurate)
#   2. pypdf        — digital PDF fallback
#   3. pytesseract  — scanned/image PDFs (requires tesseract-ocr)
#   4. easyocr      — last resort OCR
# ============================================================

import re
import os


def extract_text_from_pdf(pdf_path):
    """Auto-detect PDF type and extract text. Returns raw string."""

    # ── Method 1: pdfplumber ─────────────────────────────────
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            text += " ".join([str(c) for c in row if c]) + "\n"
        if len(text.strip()) > 50:
            print(f"[extractor] pdfplumber OK ({len(text)} chars)")
            return text
    except Exception as e:
        print(f"[extractor] pdfplumber: {e}")

    # ── Method 2: pypdf ──────────────────────────────────────
    try:
        import pypdf
        text = ""
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        if len(text.strip()) > 50:
            print(f"[extractor] pypdf OK ({len(text)} chars)")
            return text
    except Exception as e:
        print(f"[extractor] pypdf: {e}")

    # ── Method 3: pytesseract ────────────────────────────────
    try:
        import pypdfium2 as pdfium
        import pytesseract
        doc = pdfium.PdfDocument(pdf_path)
        text = ""
        for page in doc:
            bitmap = page.render(scale=2.5)
            img    = bitmap.to_pil()
            t      = pytesseract.image_to_string(img, config='--psm 6')
            text  += t + "\n"
        if len(text.strip()) > 50:
            print(f"[extractor] pytesseract OK ({len(text)} chars)")
            return text
    except Exception as e:
        print(f"[extractor] pytesseract: {e}")

    # ── Method 4: easyocr ────────────────────────────────────
    try:
        import pypdfium2 as pdfium
        import easyocr
        import numpy as np
        doc    = pdfium.PdfDocument(pdf_path)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        text   = ""
        for page in doc:
            bitmap = page.render(scale=2.0)
            img    = bitmap.to_pil()
            result = reader.readtext(np.array(img), detail=0)
            text  += "\n".join(result) + "\n"
        if len(text.strip()) > 50:
            print(f"[extractor] easyocr OK ({len(text)} chars)")
            return text
    except Exception as e:
        print(f"[extractor] easyocr: {e}")

    print("[extractor] All methods failed")
    return ""


# ─────────────────────────────────────────────────────────────
#  OCR NORMALIZER — fix known OCR artifacts before regex parsing
# ─────────────────────────────────────────────────────────────

def normalize_ocr(text):
    """
    Correct OCR artifacts observed in real lab PDFs.
    Call this before all regex matching.
    """
    text = re.sub(r'[ \t]+', ' ', text)             # collapse whitespace
    text = re.sub(r'(\d),(\d)', r'\1.\2', text)      # "12,5" → "12.5"
    text = re.sub(r'[©¢°]', ':', text)               # SRN: © → : in field separators
    text = re.sub(r'\bROW\b', 'RDW', text)           # Crystal: OCR misread
    text = re.sub(r'Eosinophit[sl]+', 'Eosinophils', text, flags=re.IGNORECASE)  # Crystal OCR
    text = re.sub(r'[Hh]ematrocrit', 'Hematocrit', text)   # SRN typo
    text = re.sub(r'EDTA\s*blood', '', text, flags=re.IGNORECASE)  # SRN: remove noise after WBC value
    # SRN: Hemoglobin line becomes garbled junk when printed bold — neutralize it
    # so downstream patterns don't produce wrong values
    text = re.sub(r'([Hh]a?emoglobin)\s+[^\d\n]{20,}', r'\1 ', text)
    return text


# ─────────────────────────────────────────────────────────────
#  CBC VALUE EXTRACTOR
# ─────────────────────────────────────────────────────────────

def extract_cbc_values(raw_text):
    """
    Extract 14 CBC parameter values from text.
    Returns dict: {parameter_name: float_value}
    """
    text = normalize_ocr(raw_text)

    patterns = {

        "Hemoglobin": [
            # Match value on SAME LINE only (stops at newline) — prevents
            # SRN's garbled Hb line from grabbing next line's RBC value
            r"[Hh]a?emoglobin\s*\(?Hb\)?[^\d\n]*([\d.]+)",
            r"[Hh]a?emoglobin[^\d\n]*([\d.]+)",
            r"\bHb\b[^\d\n]*([\d.]+)",
            r"\bHGB\b[^\d\n]*([\d.]+)",
        ],

        "PCV": [
            r"Packed\s*Cell\s*Volume\s*\(?PCV\)?[^\d]*([\d.]+)",
            r"\bPCV\b[^\d]*([\d.]+)",
            r"[Hh]a?ematocrit[^\d]*([\d.]+)",   # SRN: Hematocrit / Hematrocrit (normalized)
            r"\b[Hh][Cc][Tt]\b[^\d]*([\d.]+)",  # Flabs: Hct
            r"\bHCT\b[^\d]*([\d.]+)",
        ],

        # WBC: Flabs=Total Leucocyte Count, Crystal=Total WBC Count,
        #      SRN=TOTAL COUNT (WBC) [EDTAblood stripped by normalizer]
        "WBC": [
            r"Total\s*[Ll]eu[ck]ocyte\s*[Cc]ount[^\d]*([\d.]+)",
            r"Total\s*WBC\s*[Cc]ount[^\d]*([\d.]+)",
            r"TOTAL\s*COUNT\s*\(WBC\)[^\d]*([\d.]+)",
            r"\bWBC\b[^\d]*([\d.]+)",
            r"[Ww]hite\s*[Bb]lood\s*[Cc]ell[^\d]*([\d.]+)",
            r"[Ll]eu[ck]ocyte\s*[Cc]ount[^\d]*([\d.]+)",
            r"\bTLC\b[^\d]*([\d.]+)",
            r"\bWCC\b[^\d]*([\d.]+)",
        ],

        "RBC": [
            r"Total\s*RBC\s*[Cc]ount[^\d]*([\d.]+)",
            r"RBC\s*[Cc]ount[^\d]*([\d.]+)",
            r"\bRBC\b[^\d]*([\d.]+)",
            r"[Rr]ed\s*[Bb]lood\s*[Cc]ell[^\d]*([\d.]+)",
            r"[Ee]rythrocyte[^\d]*([\d.]+)",
        ],

        # Platelets: SRN=116 (10³/µL), Crystal=1550000 (OCR of 155,000)
        "Platelets": [
            r"PLATELET\s*COUNT[^\d]*([\d,]+)",
            r"[Pp]latelet\s*[Cc]ount[^\d]*([\d,]+)",
            r"[Pp]latelets\b[^\d]*([\d,]+)",
            r"\bPLT\b[^\d]*([\d,]+)",
        ],

        "MCV": [
            r"Mean\s*Corpuscular\s*Volume\s*\(?MCV\)?[^\d]*([\d.]+)",
            r"\bMCV\b[^\d]*([\d.]+)",
        ],

        "MCH": [
            r"Mean\s*Corpuscular\s*[Hh]a?emo[a-z]*\b[^\d]*([\d.]+)",
            r"\bMCH\b[^C\d\s][^\d]*([\d.]+)",
            r"\bMCH\b\s*[\n\r]+[^\d]*([\d.]+)",
            r"\bMCH\b\s+([\d.]+)",
        ],

        "MCHC": [
            r"Mean\s*Corpuscular\s*[Hh]a?emo[a-z]*\s*Conc[^\d]*([\d.]+)",
            r"\bMCHC\b[^\d]*([\d.]+)",
        ],

        # RDW: Flabs="RDW-CV 12", SRN="RDW- CV 13.7", Crystal="ROW 10"→normalized
        "RDW": [
            r"\bRDW[-\s_]CV\b[^\d]*([\d.]+)",
            r"[Rr]ed\s*[Cc]ell\s*[Dd]istribution[^\d]*([\d.]+)",
            r"\bRDW\b[^\d]*([\d.]+)",
        ],

        # Differential counts — SRN uses "Neutrophils (%)" format
        "Neutrophils": [
            r"[Nn]eutrophil[s]?\s*\(?%?\)?[^\d]*([\d.]+)",
            r"\bNeut\b[^\d]*([\d.]+)",
            r"\bPMN\b[^\d]*([\d.]+)",
        ],

        "Lymphocytes": [
            r"[Ll]ymphocyte[s]?\s*\(?%?\)?[^\d]*([\d.]+)",
            r"\bLymph\b[^\d]*([\d.]+)",
            r"\bLYM\b[^\d]*([\d.]+)",
        ],

        "Eosinophils": [
            r"[Ee]osinophil[s]?\s*\(?%?\)?[^\d]*([\d.]+)",  # also catches "Eosinophits" after normalize
            r"\bEos\b[^\d]*([\d.]+)",
        ],

        "Monocytes": [
            r"[Mm]onocyte[s]?\s*\(?%?\)?[^\d]*([\d.]+)",
            r"\bMono\b[^\d]*([\d.]+)",
        ],

        "Basophils": [
            r"[Bb]asophil[s]?\s*\(?%?\)?[^\d]*([\d.]+)",
            r"\bBaso\b[^\d]*([\d.]+)",
        ],
    }

    zero_allowed = {"Basophils", "Eosinophils"}
    values = {}

    for param, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text)
            if match:
                raw = match.group(1).replace(",", "")
                try:
                    val = float(raw)
                    if val > 0 or param in zero_allowed:
                        values[param] = val
                        break
                except ValueError:
                    continue

    # ── Unit scaling ─────────────────────────────────────────
    # WBC: if < 50, lab reported in 10³/µL → ×1000
    if "WBC" in values and values["WBC"] < 50:
        values["WBC"] = round(values["WBC"] * 1000)

    # Platelets:
    #   < 2000 → 10³/µL → ×1000   (SRN: 116 → 116000)
    #   > 900k → OCR dropped comma (Crystal: 1550000 → 155000)
    if "Platelets" in values:
        plt = values["Platelets"]
        if plt < 2000:
            values["Platelets"] = round(plt * 1000)
        elif plt > 900000:
            candidate = round(plt / 10)
            if 10000 <= candidate <= 900000:
                values["Platelets"] = candidate

    # ── Hemoglobin fallback ───────────────────────────────────
    # SRN: bold Hemoglobin text gets garbled by OCR.
    # Estimate from PCV if Hb is missing (Hb ≈ PCV / 3).
    if "Hemoglobin" not in values and "PCV" in values:
        est = round(values["PCV"] / 3.0, 1)
        if 3.0 <= est <= 25.0:
            values["Hemoglobin"] = est
            print(f"[extractor] Hemoglobin estimated from PCV: {est} g/dL")

    return values


# ─────────────────────────────────────────────────────────────
#  PATIENT INFO EXTRACTOR
# ─────────────────────────────────────────────────────────────

def extract_patient_info(raw_text):
    """
    Extract name, age, gender from report header.
    Handles: Flabs, Drlogy, SRN Diagnostics, Crystal Data Inc.
    """
    text = normalize_ocr(raw_text)
    info = {"name": "Unknown", "age": None, "gender": "Male"}

    # ── Name ─────────────────────────────────────────────────
    name_patterns = [
        # Crystal Data: "PATIENT NAME : MR. KETAN CHAVAN  SEX : Male"
        # Negative lookahead stops before SEX, AGE, etc.
        r"PATIENT\s*NAME\s*[:\-]\s*(?:MR\.?\s*|MRS\.?\s*|MS\.?\s*)?([A-Z][A-Z]+(?:\s(?!SEX|AGE|DATE|REF|LAB|SAMPLE)[A-Z][A-Z]+){1,3})",

        # SRN: "Patient MR. TRIJUGEE NARAYAN SHUKLA  Reg. No."
        r"^Patient\s+(?:MR\.?\s*|MRS\.?\s*|MS\.?\s*)([A-Z][A-Z]+(?:\s[A-Z][A-Z]+){1,4})",

        # Flabs: "Name : Mr Dummy Patient ID"
        r"(?:^|\n)\s*Name\s*[:\-]\s*(?:Mr\.?\s*|Mrs\.?\s*|Ms\.?\s*|Dr\.?\s*)([A-Z][a-zA-Z]+(?:\s(?!Patient|Report|ID|Age|Gender|Phone|Ref)[A-Z][a-zA-Z]+){0,2})",

        # Drlogy: "Patient Name : Yash M. Patel"
        r"Patient\s*Name\s*[:\-]\s*([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z.]+){0,2})",

        # Bold name at start of line (Drlogy standalone header)
        r"^([A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+)",
        r"^([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+)",
        r"^([A-Z][a-z]+\s+[A-Z][a-z]+)",
    ]

    SKIP_WORDS = [
        "PATHOLOGY", "LAB", "HOSPITAL", "CLINIC", "REPORT",
        "BLOOD", "COMPLETE", "INVESTIGATION", "SAMPLE",
        "LEUCOCYTE", "LEUKOCYTE", "HAEMATOLOGY", "HEMATOLOGY",
        "PLATELET", "NEUTROPHIL", "LYMPHOCYTE", "HAEMOGLOBIN",
        "HEMOGLOBIN", "COUNT", "DIFFERENTIAL", "ABSOLUTE",
        "TOTAL", "RBC", "WBC", "CBC", "INDICES", "TEST",
        "RESULT", "RANGE", "UNIT", "DESCRIPTION", "PATIENT",
        "MBBS", "DMLT", "BMLT", "PATHOLOGIST", "TECHNICIAN",
        "CONSULTING", "DEVELOPMENT", "SUPPORT", "DIAGNOSTICS",
        "DOCTOR", "PHYSICIAN",
    ]

    for pattern in name_patterns:
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            candidate = m.group(1).strip().split('\n')[0].strip()
            if not any(w in candidate.upper() for w in SKIP_WORDS):
                info["name"] = candidate
                break

    # ── Age + Gender ─────────────────────────────────────────
    # Flabs/SRN: "Age/Gender : 20/Male"  or  "Age/Gender : 68 Y/Male"
    m = re.search(r"Age[/\s]*Gender\s*[:\-]?\s*(\d+)\s*[Yy]?\.?\s*/\s*(\w+)", text)
    if m:
        info["age"]    = int(m.group(1))
        info["gender"] = "Female" if "female" in m.group(2).lower() else "Male"
    else:
        # Crystal/Drlogy: "AGE : 29 Years" or "Age : 21 Years"
        m = re.search(r"[Aa][Gg][Ee]\s*[:\-]?\s*(\d+)", text)
        if m:
            info["age"] = int(m.group(1))
        # Gender: check SEX field first, then Male/Female anywhere
        sex_m = re.search(r"\bSEX\s*[:\-]\s*(\w+)", text)
        if sex_m:
            info["gender"] = "Female" if "female" in sex_m.group(1).lower() else "Male"
        elif re.search(r"\b[Ff]emale\b|\bWoman\b", text):
            info["gender"] = "Female"
        elif re.search(r"\b[Mm]ale\b|\bMan\b", text):
            info["gender"] = "Male"

    info["age_group"] = "Child" if (info["age"] and info["age"] < 18) else info["gender"]
    return info
