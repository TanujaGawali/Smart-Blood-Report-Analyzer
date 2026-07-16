# ============================================================
#   SMART BLOOD REPORT ANALYZER — Main Streamlit App
# ============================================================

import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from extractor import extract_text_from_pdf, extract_cbc_values, extract_patient_info
from analyzer  import run_full_analysis
from pdf_report import generate_pdf_report
from hindi_translator import (
    translate_status, translate_parameter, translate_label,
    translate_score_advice, get_hindi_disease_info
)

st.set_page_config(page_title="Smart Blood Report Analyzer", page_icon="🩸", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;}

.main-header{background:linear-gradient(135deg,#c0392b,#8e1a1a);border-radius:20px;padding:2.5rem;text-align:center;margin-bottom:2rem;box-shadow:0 8px 32px rgba(192,57,43,0.4);}
.main-header h1{font-family:'Outfit',sans-serif;font-size:2.6rem;font-weight:800;color:white;margin:0;}
.main-header p{color:rgba(255,255,255,0.85);font-size:1rem;margin:0.5rem 0 0 0;}

.card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:1.5rem;margin-bottom:1.2rem;}
.card h3{color:#fff;font-family:'Outfit',sans-serif;font-weight:700;margin-top:0;}
.card p,.card li{color:rgba(255,255,255,0.8);line-height:1.7;}

.score-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border:2px solid;border-radius:20px;padding:2rem;text-align:center;margin:1rem 0;}
.score-number{font-family:'Outfit',sans-serif;font-size:4.5rem;font-weight:800;line-height:1;}
.score-label{font-size:1.3rem;font-weight:600;margin-top:0.5rem;}
.score-advice{color:rgba(255,255,255,0.75);font-size:0.9rem;margin-top:0.8rem;}

.param-row{display:flex;justify-content:space-between;align-items:center;padding:0.7rem 1rem;border-radius:10px;margin-bottom:0.5rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);}
.param-name{color:#ddd;font-weight:500;min-width:140px;}
.param-value{font-weight:700;font-size:1.05rem;min-width:120px;}
.param-ref{color:rgba(255,255,255,0.5);font-size:0.85rem;min-width:130px;}

.status-normal{color:#2ecc71;} .status-borderline{color:#f39c12;} .status-abnormal{color:#e74c3c;} .status-critical{color:#ff4757;}

.disease-card{background:rgba(255,255,255,0.04);border-left:4px solid #e74c3c;border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin-bottom:1rem;}
.disease-card h4{color:#fff;font-family:'Outfit',sans-serif;font-weight:700;margin:0 0 0.5rem 0;}
.confidence-bar{background:rgba(255,255,255,0.1);border-radius:20px;height:8px;margin:0.5rem 0;overflow:hidden;}
.confidence-fill{height:100%;border-radius:20px;background:linear-gradient(90deg,#e74c3c,#c0392b);}

.food-eat{color:#2ecc71;} .food-avoid{color:#e74c3c;} .medicine{color:#3498db;} .lifestyle{color:#f39c12;}

.disclaimer{background:rgba(231,76,60,0.15);border:1px solid rgba(231,76,60,0.4);border-radius:12px;padding:1rem 1.5rem;margin-top:2rem;color:rgba(255,255,255,0.8);font-size:0.9rem;}

.metric-box{background:rgba(255,255,255,0.06);border-radius:14px;padding:1.2rem;text-align:center;border:1px solid rgba(255,255,255,0.1);}
.metric-val{font-family:'Outfit',sans-serif;font-size:1.8rem;font-weight:800;color:#fff;word-break:break-word;}
.metric-label{font-size:0.85rem;color:rgba(255,255,255,0.55);margin-top:4px;}

.stButton>button{background:linear-gradient(135deg,#c0392b,#8e1a1a);color:white;border:none;border-radius:12px;padding:0.7rem 2rem;font-weight:600;font-size:1rem;width:100%;}
.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(255,255,255,0.05);border-radius:12px;padding:6px;}
.stTabs [data-baseweb="tab"]{border-radius:8px;color:rgba(255,255,255,0.6);font-weight:500;}
.stTabs [aria-selected="true"]{background:#c0392b !important;color:white !important;}
h1,h2,h3,h4{color:white;} label{color:white !important;}
</style>
""", unsafe_allow_html=True)


# ─── RESULTS DISPLAY ─────────────────────────────────────────
def display_results(results, values, patient_info=None, show_hindi=False):
    st.markdown("---")

    # ── Top action bar ────────────────────────────────────────
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("## 📊 Analysis Results")
    with col_btn:
        if patient_info:
            try:
                pdf_bytes = generate_pdf_report(patient_info, results)
                patient_name = patient_info.get("name", "Patient").replace(" ", "_")
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"Blood_Report_{patient_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.caption(f"PDF error: {e}")

    # ML model badge
    method = results.get("prediction_method", "rule-based")
    ml_info = results.get("ml_info")
    if method == "ml" and ml_info:
        st.markdown(f"""
        <div style="display:inline-block;background:linear-gradient(135deg,#1a1a2e,#16213e);
             border:1px solid rgba(52,152,219,0.5);border-radius:10px;
             padding:0.5rem 1.2rem;margin-bottom:1rem;">
            <span style="color:#3498db;font-weight:600;">🤖 ML Model Active</span>
            <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;margin-left:1rem;">
                Random Forest &nbsp;|&nbsp; Accuracy: {ml_info['accuracy']}% &nbsp;|&nbsp;
                F1: {ml_info['f1_score']}% &nbsp;|&nbsp; CV: {ml_info['cv_mean']}%
            </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:inline-block;background:rgba(255,255,255,0.05);
             border:1px solid rgba(255,255,255,0.15);border-radius:10px;
             padding:0.5rem 1.2rem;margin-bottom:1rem;">
            <span style="color:#f39c12;font-weight:600;">⚙️ Rule-based Engine</span>
            <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;margin-left:1rem;">
                ML model not found — run train_model.py to enable ML predictions
            </span>
        </div>""", unsafe_allow_html=True)

    score  = results["health_score"]
    label  = results["score_label"]
    advice = results["score_advice"]

    if   score >= 90: sc = bc = "#2ecc71"
    elif score >= 75: sc = bc = "#27ae60"
    elif score >= 60: sc = bc = "#f39c12"
    elif score >= 40: sc = bc = "#e67e22"
    else:             sc = bc = "#e74c3c"

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="score-card" style="border-color:{bc}">
            <div class="score-number" style="color:{sc}">{score}</div>
            <div style="color:rgba(255,255,255,0.5);font-size:1rem;">out of 100</div>
            <div class="score-label" style="color:{sc}">{label}</div>
            <div class="score-advice">{advice}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        abnormal = [a for a in results["abnormalities"] if a["status"] != "Normal"]
        normal_p = [a for a in results["abnormalities"] if a["status"] == "Normal"]
        st.markdown(f"""
        <div class="card">
            <h3>📈 Summary</h3>
            <p>🟢 <strong>Normal Parameters:</strong> {len(normal_p)}<br>
               🔴 <strong>Abnormal Parameters:</strong> {len(abnormal)}<br>
               🦠 <strong>Predicted Conditions:</strong> {len(results['diseases'])}</p>
        </div>""", unsafe_allow_html=True)

        if results["diseases"]:
            top = results["diseases"][0]
            st.markdown(f"""
            <div class="disease-card">
                <h4>🔍 Top Predicted Condition</h4>
                <p style="color:rgba(255,255,255,0.75);margin:0">{top['name']} — <strong style="color:#e74c3c">{top['confidence']}% confidence</strong></p>
                <p style="color:rgba(255,255,255,0.6);font-size:0.85rem;margin-top:0.4rem">⏰ {top['urgency']}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CBC parameters
    st.markdown("### 🧪 CBC Parameter Details")
    for item in results["abnormalities"]:
        s = item["status"]
        css = "status-normal" if "Normal" in s else "status-borderline" if "Borderline" in s else "status-critical" if "Critical" in s else "status-abnormal"
        param_display  = f"{translate_parameter(item['parameter'])} ({item['parameter']})" if show_hindi else item['parameter']
        status_display = translate_status(item['status']) if show_hindi else item['status']
        st.markdown(f"""
        <div class="param-row">
            <span class="param-name">{param_display}</span>
            <span class="param-value {css}">{item['value']} {item['unit']}</span>
            <span class="param-ref">Ref: {item['low']} – {item['high']}</span>
            <span class="{css}">{item['color']} {status_display}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Disease details
    if results["diseases"]:
        st.markdown("### 🦠 Predicted Conditions & Health Advice")
        for disease in results["diseases"]:
            hindi_info = get_hindi_disease_info(disease["name"]) if show_hindi else None
            display_name = f"{disease['name']}" if not show_hindi else f"{translate_label(disease['name'])} ({disease['name']})"
            with st.expander(f"🔍 {display_name}  —  {disease['confidence']}% Confidence", expanded=True):
                st.markdown(f"""<div class="confidence-bar"><div class="confidence-fill" style="width:{disease['confidence']}%"></div></div>""", unsafe_allow_html=True)

                cl, cr = st.columns(2)
                # Use Hindi info if toggle is on and Hindi info exists
                desc      = (hindi_info["description"] if hindi_info else disease["description"])
                urgency   = (hindi_info["urgency"]     if hindi_info else disease["urgency"])
                doctor    = (hindi_info["doctor"]      if hindi_info else disease["doctor"])
                foods_eat = (hindi_info["foods_eat"]   if hindi_info else disease["foods_eat"])
                foods_avoid=(hindi_info["foods_avoid"] if hindi_info else disease["foods_avoid"])
                medicines = (hindi_info["medicines"]   if hindi_info else disease["medicines"])
                lifestyle = (hindi_info["lifestyle"]   if hindi_info else disease["lifestyle"])

                what_label = "यह बीमारी क्या है?" if show_hindi else "What is this condition?"
                urg_label  = "⏰ तात्कालिकता और डॉक्टर" if show_hindi else "⏰ Urgency & Doctor"
                life_label = "🏃 जीवनशैली सुझाव" if show_hindi else "🏃 Lifestyle Tips"
                eat_label  = "🥗 खाने योग्य भोजन" if show_hindi else "🥗 Foods to EAT"
                avoid_label= "🚫 परहेज करने वाले भोजन" if show_hindi else "🚫 Foods to AVOID"
                med_label  = "💊 दवाइयाँ" if show_hindi else "💊 Common Medications"
                when_label = "कब जाएं:" if show_hindi else "When to act:"
                consult_lbl= "सलाह लें:" if show_hindi else "Consult:"

                with cl:
                    st.markdown(f"""<div class="card"><h3>📖 {what_label}</h3><p>{desc}</p></div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="card"><h3>{urg_label}</h3><p>🕐 <strong>{when_label}</strong> {urgency}</p><p>🏥 <strong>{consult_lbl}</strong> {doctor}</p></div>""", unsafe_allow_html=True)
                    if lifestyle:
                        tips = "".join([f"<li class='lifestyle'>🌿 {t}</li>" for t in lifestyle])
                        st.markdown(f"""<div class="card"><h3>{life_label}</h3><ul>{tips}</ul></div>""", unsafe_allow_html=True)

                with cr:
                    if foods_eat:
                        items = "".join([f"<li class='food-eat'>✅ {f}</li>" for f in foods_eat])
                        st.markdown(f"""<div class="card"><h3>{eat_label}</h3><ul>{items}</ul></div>""", unsafe_allow_html=True)
                    if foods_avoid:
                        items = "".join([f"<li class='food-avoid'>❌ {f}</li>" for f in foods_avoid])
                        st.markdown(f"""<div class="card"><h3>{avoid_label}</h3><ul>{items}</ul></div>""", unsafe_allow_html=True)
                    if medicines:
                        items = "".join([f"<li class='medicine'>💊 {m}</li>" for m in medicines])
                        st.markdown(f"""<div class="card"><h3>{med_label}</h3><p style="color:rgba(255,255,255,0.5);font-size:0.8rem;">⚠️ {'डॉक्टर की सलाह के बिना कोई दवा न लें' if show_hindi else 'Consult your doctor before taking any medication'}</p><ul>{items}</ul></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="card"><h3>✅ No Significant Conditions Predicted</h3><p>Your CBC values appear to be within normal ranges. Keep maintaining a healthy lifestyle!</p></div>""", unsafe_allow_html=True)

    if show_hindi:
        st.markdown("""
        <div class="disclaimer">
            <strong>⚠️ चिकित्सा अस्वीकरण:</strong> यह उपकरण केवल <strong>शैक्षिक उद्देश्यों के लिए</strong> है।
            यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है। हमेशा एक योग्य डॉक्टर से परामर्श लें।
            आपातकाल में: <strong>108</strong> पर कॉल करें।
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong> This tool is for <strong>educational and informational purposes only</strong>.
            It does NOT replace professional medical advice. Always consult a certified doctor.
            Emergency: call <strong>108</strong> (India).
        </div>""", unsafe_allow_html=True)


# ─── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🩸 Smart Blood Report Analyzer</h1>
    <p>Upload your CBC blood report PDF — get instant disease insights, health score & diet advice</p>
</div>""", unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Patient Settings")
    patient_gender = st.selectbox("Patient Gender", ["Male", "Female"])
    patient_age    = st.number_input("Patient Age", min_value=1, max_value=120, value=21)
    age_group = "Child" if patient_age < 18 else patient_gender
    st.markdown("---")
    st.markdown("""
    **This tool analyzes CBC reports:**
    - 🦠 Disease predictions
    - 📊 Health score / 100
    - 🥗 Food & diet advice
    - 💊 Medication suggestions
    - 🏥 Doctor type recommendations
    """)
    st.caption("⚠️ Educational purposes only. Always consult a doctor.")
    st.markdown("---")
    st.markdown("### 🌐 Language / भाषा")
    show_hindi = st.toggle("हिंदी में दिखाएं (Show in Hindi)", value=False)


# ─── TABS ─────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📤 Upload PDF Report", "✏️ Enter Values Manually"])

# TAB 1 — PDF
with tab1:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border:2px dashed rgba(192,57,43,0.6);border-radius:20px;padding:2rem;text-align:center;margin:1rem 0;">
        <h3 style="color:white;font-family:'Outfit',sans-serif;">📄 Upload Your Blood Report PDF</h3>
        <p style="color:rgba(255,255,255,0.6);">Supports digital PDFs (hospital-generated) and scanned PDFs</p>
    </div>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        import tempfile, os
        tmp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("📄 Reading PDF..."):
            raw_text = extract_text_from_pdf(tmp_path)

        if not raw_text.strip():
            st.error("❌ Could not extract text from this PDF.")
            st.info("💡 This usually means the PDF is image-only and poppler is not installed, OR the PDF is password-protected.")
            with st.expander("🔧 How to fix"):
                st.markdown("""
                **Option 1 — Install poppler (for scanned PDFs):**
                1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
                2. Extract zip to `C:\\poppler`
                3. Add `C:\\poppler\\Library\\bin` to your System PATH
                4. Restart terminal and try again

                **Option 2 — Use Manual Entry tab** (fastest!)
                Just type your CBC values directly — no PDF needed.
                """)
        else:
            with st.spinner("🔍 Extracting CBC values..."):
                values   = extract_cbc_values(raw_text)
                pat_info = extract_patient_info(raw_text)

            # Debug expander — shows raw extracted text
            with st.expander("🔍 Debug: View extracted text (click to expand)"):
                st.text(raw_text[:2000])

            if len(values) < 2:
                st.warning("⚠️ Extracted only a few values. Try manual entry for better results.")
                with st.expander("🔍 Debug: Values found"):
                    st.write(values)

            if values:
                st.success(f"✅ Extracted {len(values)} parameters from your report!")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""<div class="metric-box"><div class="metric-val">{pat_info['name']}</div><div class="metric-label">Patient Name</div></div>""", unsafe_allow_html=True)
                with c2:
                    age_d = f"{pat_info['age']} yrs" if pat_info['age'] else f"{patient_age} yrs"
                    st.markdown(f"""<div class="metric-box"><div class="metric-val">{age_d}</div><div class="metric-label">Age</div></div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="metric-box"><div class="metric-val">{pat_info['gender']}</div><div class="metric-label">Gender</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                eff_group = pat_info.get("age_group", age_group)
                results = run_full_analysis(values, eff_group)
                display_results(results, values, pat_info, show_hindi)

# TAB 2 — Manual
with tab2:
    st.markdown("### 📝 Enter CBC Values Manually")
    st.caption("Enter values from your report. Leave as 0 to skip.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🔴 Core Parameters**")
        hb  = st.number_input("Hemoglobin (g/dL)",       0.0, 25.0,     0.0, 0.1)
        pcv = st.number_input("PCV / Hematocrit (%)",    0.0, 80.0,     0.0, 0.1)
        rbc = st.number_input("RBC Count (mill/cumm)",   0.0, 10.0,     0.0, 0.1)
        wbc = st.number_input("WBC Count (cumm)",        0.0, 100000.0, 0.0, 100.0)
        plt = st.number_input("Platelet Count (cumm)",   0.0, 1000000.0,0.0, 1000.0)
    with c2:
        st.markdown("**🟡 Blood Indices**")
        mcv  = st.number_input("MCV (fL)",    0.0, 150.0, 0.0, 0.1)
        mch  = st.number_input("MCH (pg)",    0.0, 50.0,  0.0, 0.1)
        mchc = st.number_input("MCHC (g/dL)", 0.0, 45.0,  0.0, 0.1)
        rdw  = st.number_input("RDW (%)",     0.0, 30.0,  0.0, 0.1)
    with c3:
        st.markdown("**🟢 Differential WBC**")
        neu = st.number_input("Neutrophils (%)", 0.0, 100.0, 0.0, 0.1)
        lym = st.number_input("Lymphocytes (%)", 0.0, 100.0, 0.0, 0.1)
        eos = st.number_input("Eosinophils (%)", 0.0, 30.0,  0.0, 0.1)
        mon = st.number_input("Monocytes (%)",   0.0, 20.0,  0.0, 0.1)
        bas = st.number_input("Basophils (%)",   0.0, 5.0,   0.0, 0.1)

    if st.button("🔍 Analyze My Report"):
        manual_values = {k: v for k, v in [
            ("Hemoglobin", hb), ("PCV", pcv), ("RBC", rbc),
            ("WBC", wbc), ("Platelets", plt), ("MCV", mcv),
            ("MCH", mch), ("MCHC", mchc), ("RDW", rdw),
            ("Neutrophils", neu), ("Lymphocytes", lym),
            ("Eosinophils", eos), ("Monocytes", mon), ("Basophils", bas),
        ] if v > 0}

        if len(manual_values) < 2:
            st.error("⚠️ Please enter at least 2 values to analyze.")
        else:
            pat_info_manual = {"name": "Patient", "age": patient_age, "gender": patient_gender}
            results = run_full_analysis(manual_values, age_group)
            display_results(results, manual_values, pat_info_manual, show_hindi)


st.markdown("""
<br><br>
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.85rem;">
    🩸 Smart Blood Report Analyzer &nbsp;|&nbsp; NLP B.Tech Project &nbsp;|&nbsp; Python • spaCy • Streamlit
</div>""", unsafe_allow_html=True)