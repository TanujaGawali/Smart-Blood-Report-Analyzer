# ============================================================
#   DISEASE DATABASE — Explanations, Foods, Medicines, Advice
# ============================================================

DISEASE_DB = {

    "Iron Deficiency Anemia": {
        "description": (
            "Anemia means your blood doesn't have enough healthy red blood cells. "
            "Iron deficiency anemia happens when your body lacks enough iron to produce "
            "hemoglobin — the protein in red blood cells that carries oxygen throughout your body. "
            "This is the most common type of anemia in India, especially in women and young people."
        ),
        "severity_info": {
            "Mild":     "Not an emergency. With proper diet and treatment, it improves in 4–8 weeks.",
            "Moderate": "Needs medical attention. Can cause fatigue, weakness, and poor concentration.",
            "Severe":   "Requires immediate medical care. Can affect heart function and organ health.",
        },
        "urgency": "Visit a doctor within 1 week.",
        "doctor_type": "General Physician → Hematologist (if severe)",
        "foods_eat": [
            "Spinach (Palak), Methi, and dark leafy vegetables",
            "Beetroot, Pomegranate, Watermelon",
            "Dates (Khajoor), Raisins, Jaggery (Gud)",
            "Chicken Liver, Eggs, Fish, Lean Meat",
            "Lentils (Dal), Rajma, Chickpeas (Chana)",
            "Vitamin C foods (Lemon, Orange, Amla) — help absorb iron",
            "Pumpkin seeds, Sesame seeds (Til)",
        ],
        "foods_avoid": [
            "Tea and Coffee (block iron absorption — avoid 1 hour before/after meals)",
            "Milk and dairy products taken with iron-rich meals",
            "Calcium supplements at same time as iron-rich food",
            "Processed and packaged junk food",
            "Alcohol",
        ],
        "medicines": [
            "Iron + Folic Acid tablets (e.g., Autrin, Feronia-XT, Livogen)",
            "Vitamin C tablets (helps iron absorption)",
            "Iron injections (for severe cases — only on doctor's advice)",
            "Vitamin B12 supplements (if combined deficiency)",
        ],
        "lifestyle": [
            "Sleep 7–8 hours daily",
            "Avoid intense physical exercise until levels improve",
            "Cook in iron cookware — it adds iron to food naturally",
            "Eat small, frequent meals rich in iron",
        ],
    },

    "Polycythemia / Dehydration": {
        "description": (
            "Polycythemia means your blood has too many red blood cells (high PCV/hematocrit). "
            "This can make your blood thicker and harder to pump. "
            "In young people, it is often caused by dehydration. "
            "In more serious cases, it can be a bone marrow disorder."
        ),
        "severity_info": {
            "Mild":     "Likely simple dehydration. Drink more water and retest.",
            "Moderate": "May need further tests to rule out bone marrow issues.",
            "Severe":   "Requires immediate hematologist evaluation.",
        },
        "urgency": "Monitor at home if mild. If persistent, visit doctor within 1 week.",
        "doctor_type": "General Physician → Hematologist",
        "foods_eat": [
            "Water — minimum 8–10 glasses per day",
            "Coconut water, Buttermilk, Lassi",
            "Fresh fruits with high water content (Watermelon, Cucumber, Orange)",
            "Omega-3 rich foods (Fish, Walnuts, Flaxseeds) — thin the blood naturally",
            "Garlic and Turmeric — natural blood thinners",
        ],
        "foods_avoid": [
            "Alcohol (causes dehydration)",
            "Excess salt (increases blood pressure)",
            "Processed meats and fatty foods",
            "Caffeine in excess (diuretic — causes water loss)",
            "Iron supplements (unless prescribed — can worsen condition)",
        ],
        "medicines": [
            "Hydroxyurea (for true polycythemia — only on doctor's advice)",
            "Aspirin (low dose to reduce clotting risk — on doctor's advice)",
            "Phlebotomy (therapeutic blood removal — for severe cases)",
            "ORS (Oral Rehydration Salts) if dehydrated",
        ],
        "lifestyle": [
            "Drink water regularly throughout the day",
            "Avoid hot environments and heavy sweating without rehydration",
            "Exercise moderately — stay active but don't overheat",
            "Quit smoking if applicable — worsens polycythemia",
        ],
    },

    "Thrombocytopenia (Low Platelets)": {
        "description": (
            "Thrombocytopenia means your platelet count is lower than normal. "
            "Platelets are tiny blood cells that help your blood clot when you're injured. "
            "Low platelets can cause easy bruising, prolonged bleeding, or in severe cases, "
            "internal bleeding. Causes include dengue fever, viral infections, or autoimmune conditions."
        ),
        "severity_info": {
            "Mild":     "Borderline low. Monitor closely. Retest in 1 week.",
            "Moderate": "Significant drop. Avoid injury. See doctor within 2 days.",
            "Severe":   "Critical — risk of spontaneous bleeding. Go to hospital immediately.",
        },
        "urgency": "See doctor within 2–3 days. Avoid injury and strenuous activity.",
        "doctor_type": "General Physician → Hematologist",
        "foods_eat": [
            "Papaya leaves juice (proven to increase platelets — especially in dengue)",
            "Papaya fruit",
            "Pomegranate and Pomegranate juice",
            "Beetroot juice",
            "Kiwi, Guava, and Vitamin C rich fruits",
            "Spinach and leafy greens",
            "Pumpkin and pumpkin seeds",
            "Milk and dairy products",
        ],
        "foods_avoid": [
            "Alcohol (severely reduces platelet count)",
            "Quinine (in tonic water)",
            "Aspirin and Ibuprofen (reduce platelet function)",
            "Processed foods with artificial preservatives",
            "Cranberry juice (in large amounts)",
        ],
        "medicines": [
            "Treat underlying cause (e.g., antiviral for dengue)",
            "Corticosteroids (for immune thrombocytopenia — doctor's advice)",
            "Platelet transfusion (for very low counts — hospital procedure)",
            "Vitamin C and folate supplements",
        ],
        "lifestyle": [
            "Avoid contact sports and activities that risk injury",
            "Use soft toothbrush to avoid gum bleeding",
            "Avoid sharp objects and be careful in daily activities",
            "Rest adequately and avoid stress",
        ],
    },

    "Leukocytosis (High WBC — Infection)": {
        "description": (
            "Leukocytosis means your white blood cell count is higher than normal. "
            "WBCs are your body's soldiers against infection. High WBC usually means "
            "your body is actively fighting a bacterial or viral infection, inflammation, "
            "or stress. Rarely, it can indicate blood cancers like leukemia."
        ),
        "severity_info": {
            "Mild":     "Common during minor infections. Should normalize after recovery.",
            "Moderate": "Active infection present. Needs diagnosis and treatment.",
            "Severe":   "Very high WBC. Could indicate serious infection or blood disorder. Go to hospital.",
        },
        "urgency": "See a doctor within 2–3 days to identify the infection source.",
        "doctor_type": "General Physician → Infectious Disease Specialist / Hematologist",
        "foods_eat": [
            "Turmeric milk (anti-inflammatory)",
            "Ginger and Garlic (natural antibiotics)",
            "Vitamin C foods (Lemon, Amla, Orange)",
            "Probiotic foods (Curd, Yogurt, Buttermilk)",
            "Green tea (antioxidant)",
            "Plenty of water and fluids",
            "Zinc-rich foods (Pumpkin seeds, Chickpeas, Cashews)",
        ],
        "foods_avoid": [
            "Sugar and sugary drinks (feed harmful bacteria)",
            "Processed and fried foods (increase inflammation)",
            "Alcohol (weakens immune system)",
            "Raw or undercooked meat/eggs (risk of infection)",
        ],
        "medicines": [
            "Antibiotics (if bacterial infection — only on doctor's prescription)",
            "Antivirals (if viral cause)",
            "Anti-inflammatory medications if needed",
            "Treatment depends entirely on the underlying cause",
        ],
        "lifestyle": [
            "Get adequate rest — your body is fighting infection",
            "Stay hydrated with water and soups",
            "Maintain hygiene to prevent secondary infections",
            "Monitor temperature — fever indicates active infection",
        ],
    },

    "Leukopenia (Low WBC — Weak Immunity)": {
        "description": (
            "Leukopenia means your white blood cell count is below normal. "
            "This weakens your immune system, making you more vulnerable to infections. "
            "It can be caused by viral infections, nutritional deficiencies, autoimmune "
            "diseases, or as a side effect of certain medications."
        ),
        "severity_info": {
            "Mild":     "Monitor closely. Avoid sick people and crowded places.",
            "Moderate": "Increased infection risk. See doctor within a week.",
            "Severe":   "Severely compromised immunity. Seek immediate medical care.",
        },
        "urgency": "See doctor within 3–5 days.",
        "doctor_type": "General Physician → Hematologist / Immunologist",
        "foods_eat": [
            "Protein-rich foods (Eggs, Chicken, Dal, Paneer)",
            "Vitamin B12 foods (Eggs, Meat, Dairy, Fortified cereals)",
            "Folate-rich foods (Spinach, Broccoli, Lentils)",
            "Zinc-rich foods (Pumpkin seeds, Chickpeas)",
            "Vitamin D sources (Sunlight, Milk, Fish)",
            "Probiotic foods (Curd, Yogurt)",
        ],
        "foods_avoid": [
            "Alcohol (suppresses bone marrow — reduces WBC production)",
            "Raw or undercooked food (infection risk when immunity is low)",
            "Sugary processed foods",
            "Unpasteurized dairy products",
        ],
        "medicines": [
            "Vitamin B12 injections or supplements (if deficiency)",
            "Folic acid supplements",
            "G-CSF (growth factor injections — for severe cases, hospital only)",
            "Stop causative medication if identified (only with doctor approval)",
        ],
        "lifestyle": [
            "Wash hands frequently",
            "Avoid crowded and enclosed spaces",
            "Wear mask in public if severely low",
            "Get adequate sleep — crucial for immune function",
        ],
    },

    "Thalassemia Trait": {
        "description": (
            "Thalassemia is an inherited blood disorder where the body makes an abnormal "
            "form of hemoglobin. Thalassemia trait (minor) means you carry one abnormal gene "
            "but may have mild or no symptoms. It is very common in India and often shows as "
            "mild anemia with small red blood cells."
        ),
        "severity_info": {
            "Mild":     "Thalassemia minor — usually no treatment needed. Monitor periodically.",
            "Moderate": "Thalassemia intermedia — may need occasional treatment.",
            "Severe":   "Thalassemia major — requires regular blood transfusions.",
        },
        "urgency": "Not urgent if mild. Genetic counseling recommended before marriage/pregnancy.",
        "doctor_type": "Hematologist → Genetic Counselor",
        "foods_eat": [
            "Folate-rich foods (Spinach, Lentils, Asparagus)",
            "Calcium-rich foods (Milk, Curd, Cheese)",
            "Vitamin D sources",
            "Antioxidant-rich foods (Berries, Nuts, Green tea)",
        ],
        "foods_avoid": [
            "Iron supplements (AVOID unless specifically prescribed — iron overload risk)",
            "Excess red meat (high iron)",
            "Alcohol",
            "Vitamin C in very high doses (increases iron absorption — risky)",
        ],
        "medicines": [
            "Folic acid supplements (as prescribed)",
            "Iron chelation therapy (to remove excess iron from transfusions)",
            "NO iron supplements unless specifically told by doctor",
        ],
        "lifestyle": [
            "Get genetic testing for family members",
            "Partner should also be tested before having children",
            "Regular hematologist follow-up every 6 months",
            "Carry medical information card",
        ],
    },
}


# ============================================================
#   REFERENCE RANGES FOR CBC PARAMETERS
# ============================================================

REFERENCE_RANGES = {
    "Hemoglobin": {
        "Male":   {"low": 13.0, "high": 17.0, "unit": "g/dL"},
        "Female": {"low": 12.0, "high": 15.5, "unit": "g/dL"},
        "Child":  {"low": 11.0, "high": 16.0, "unit": "g/dL"},
    },
    "PCV": {
        "Male":   {"low": 40.0, "high": 50.0, "unit": "%"},
        "Female": {"low": 36.0, "high": 46.0, "unit": "%"},
        "Child":  {"low": 35.0, "high": 45.0, "unit": "%"},
    },
    "WBC": {
        "Male":   {"low": 4000, "high": 11000, "unit": "cumm"},
        "Female": {"low": 4000, "high": 11000, "unit": "cumm"},
        "Child":  {"low": 5000, "high": 15000, "unit": "cumm"},
    },
    "RBC": {
        "Male":   {"low": 4.5, "high": 5.5, "unit": "mill/cumm"},
        "Female": {"low": 4.0, "high": 5.0, "unit": "mill/cumm"},
        "Child":  {"low": 4.0, "high": 5.2, "unit": "mill/cumm"},
    },
    "Platelets": {
        "Male":   {"low": 150000, "high": 410000, "unit": "cumm"},
        "Female": {"low": 150000, "high": 410000, "unit": "cumm"},
        "Child":  {"low": 150000, "high": 410000, "unit": "cumm"},
    },
    "MCV": {
        "Male":   {"low": 83.0, "high": 101.0, "unit": "fL"},
        "Female": {"low": 83.0, "high": 101.0, "unit": "fL"},
        "Child":  {"low": 75.0, "high": 95.0, "unit": "fL"},
    },
    "MCH": {
        "Male":   {"low": 27.0, "high": 32.0, "unit": "pg"},
        "Female": {"low": 27.0, "high": 32.0, "unit": "pg"},
        "Child":  {"low": 25.0, "high": 31.0, "unit": "pg"},
    },
    "MCHC": {
        "Male":   {"low": 32.5, "high": 34.5, "unit": "g/dL"},
        "Female": {"low": 32.5, "high": 34.5, "unit": "g/dL"},
        "Child":  {"low": 32.0, "high": 34.0, "unit": "g/dL"},
    },
    "RDW": {
        "Male":   {"low": 11.6, "high": 14.0, "unit": "%"},
        "Female": {"low": 11.6, "high": 14.0, "unit": "%"},
        "Child":  {"low": 11.6, "high": 14.0, "unit": "%"},
    },
    "Neutrophils": {
        "Male":   {"low": 50, "high": 62, "unit": "%"},
        "Female": {"low": 50, "high": 62, "unit": "%"},
        "Child":  {"low": 40, "high": 60, "unit": "%"},
    },
    "Lymphocytes": {
        "Male":   {"low": 20, "high": 40, "unit": "%"},
        "Female": {"low": 20, "high": 40, "unit": "%"},
        "Child":  {"low": 30, "high": 50, "unit": "%"},
    },
    "Eosinophils": {
        "Male":   {"low": 0, "high": 6, "unit": "%"},
        "Female": {"low": 0, "high": 6, "unit": "%"},
        "Child":  {"low": 0, "high": 8, "unit": "%"},
    },
    "Monocytes": {
        "Male":   {"low": 0, "high": 10, "unit": "%"},
        "Female": {"low": 0, "high": 10, "unit": "%"},
        "Child":  {"low": 0, "high": 10, "unit": "%"},
    },
    "Basophils": {
        "Male":   {"low": 0, "high": 2, "unit": "%"},
        "Female": {"low": 0, "high": 2, "unit": "%"},
        "Child":  {"low": 0, "high": 2, "unit": "%"},
    },
}


# ============================================================
#   EXTENDED DISEASE DATABASE — LFT, KFT, THYROID
# ============================================================

EXTENDED_DISEASE_DB = {

    # ── LIVER (LFT) ──────────────────────────────────────────
    "Fatty Liver / Hepatitis": {
        "description": (
            "The liver is inflamed or has excess fat deposits. "
            "This can be caused by alcohol, obesity, viral hepatitis, or certain medications. "
            "Common in Indians due to dietary habits."
        ),
        "severity_info": {
            "Mild":     "Fatty liver — reversible with diet and lifestyle changes.",
            "Moderate": "Significant liver stress. Needs medical evaluation.",
            "Severe":   "Possible hepatitis or cirrhosis. Immediate medical care needed.",
        },
        "urgency": "Consult a doctor within 1 week.",
        "doctor_type": "General Physician → Gastroenterologist / Hepatologist",
        "foods_eat": [
            "Green vegetables (Broccoli, Spinach, Kale)",
            "Coffee (2 cups/day — reduces liver inflammation)",
            "Oatmeal and whole grains",
            "Walnuts and healthy fats",
            "Olive oil",
            "Turmeric (curcumin — liver protective)",
            "Garlic",
        ],
        "foods_avoid": [
            "Alcohol (completely avoid)",
            "Fried and fatty foods",
            "Sugar and sugary drinks",
            "White bread, white rice (refined carbs)",
            "Red meat in excess",
            "Processed and packaged foods",
        ],
        "medicines": [
            "Silymarin / Milk Thistle (liver protective — ask doctor)",
            "Vitamin E (for non-alcoholic fatty liver — doctor's advice)",
            "Treat underlying cause (antivirals for hepatitis)",
        ],
        "lifestyle": [
            "Exercise 30 minutes daily — reduces liver fat",
            "Achieve healthy body weight",
            "Avoid alcohol completely",
            "Regular liver function tests every 3-6 months",
        ],
    },

    "Jaundice (High Bilirubin)": {
        "description": (
            "Jaundice occurs when bilirubin (a yellow pigment from broken-down red blood cells) "
            "builds up in the blood. It causes yellowing of skin and eyes. "
            "Causes include liver disease, blocked bile ducts, or excessive red blood cell breakdown."
        ),
        "severity_info": {
            "Mild":     "Mild bilirubin elevation. Monitor and investigate cause.",
            "Moderate": "Significant jaundice. Doctor visit within 2 days.",
            "Severe":   "Severe jaundice. Hospital admission may be needed.",
        },
        "urgency": "See a doctor within 2 days.",
        "doctor_type": "General Physician → Gastroenterologist",
        "foods_eat": [
            "Water and fluids (minimum 2-3 litres/day)",
            "Fresh fruit juices (Sugarcane juice — traditional remedy)",
            "Ripe papaya and mangoes",
            "Brown rice and oatmeal",
            "Buttermilk (Chaas)",
            "Coconut water",
        ],
        "foods_avoid": [
            "Alcohol (absolutely avoid)",
            "Oily and spicy food",
            "Red meat",
            "Raw/undercooked shellfish",
            "Iron supplements (can worsen)",
        ],
        "medicines": [
            "Treatment depends entirely on underlying cause",
            "Antivirals for viral hepatitis",
            "UDCA (Ursodeoxycholic acid) for bile issues — doctor only",
        ],
        "lifestyle": [
            "Complete rest during acute phase",
            "Avoid all alcohol",
            "Frequent small meals instead of large ones",
        ],
    },

    # ── KIDNEY (KFT) ─────────────────────────────────────────
    "Chronic Kidney Disease (CKD)": {
        "description": (
            "Chronic Kidney Disease means the kidneys are gradually losing their ability "
            "to filter waste and excess fluid from the blood. "
            "Common causes are diabetes, high blood pressure, and recurrent kidney infections. "
            "Very common in India — often detected late."
        ),
        "severity_info": {
            "Mild":     "Early stage — highly manageable with diet and medication.",
            "Moderate": "Significant kidney function loss. Strict medical management needed.",
            "Severe":   "Advanced CKD. May need dialysis evaluation.",
        },
        "urgency": "See a nephrologist within 1 week.",
        "doctor_type": "Nephrologist (Kidney Specialist)",
        "foods_eat": [
            "Cauliflower, Cabbage, Garlic (kidney-friendly vegetables)",
            "Egg whites (high quality protein, low phosphorus)",
            "Apples, Cranberries, Blueberries",
            "Olive oil",
            "Onions",
            "Controlled amount of water as advised by doctor",
        ],
        "foods_avoid": [
            "Bananas, Oranges, Potatoes (high potassium)",
            "Dairy in excess (high phosphorus)",
            "Processed and canned foods (high sodium)",
            "Red meat in excess",
            "Cola drinks (high phosphorus)",
            "NSAIDs like Ibuprofen (damage kidneys)",
            "Excess salt",
        ],
        "medicines": [
            "ACE inhibitors / ARBs (blood pressure control — slows CKD)",
            "Erythropoietin (for CKD-related anemia)",
            "Phosphate binders (if phosphorus is high)",
            "Vitamin D and calcium supplements as needed",
        ],
        "lifestyle": [
            "Monitor blood pressure daily",
            "Control blood sugar strictly (if diabetic)",
            "Avoid NSAIDs and self-medication",
            "Stay hydrated but within doctor's recommended limits",
            "Regular kidney function tests every 3 months",
        ],
    },

    "Kidney Stones / UTI": {
        "description": (
            "Kidney stones are hard deposits of minerals and salts that form inside the kidneys. "
            "UTI (Urinary Tract Infection) is a bacterial infection in the urinary system. "
            "Both are very common in India, especially in hot climates."
        ),
        "severity_info": {
            "Mild":     "Small stones or mild UTI — treatable with fluids and medication.",
            "Moderate": "Larger stones or severe UTI. Medical treatment needed.",
            "Severe":   "Blocked ureter or kidney infection. Hospital admission may be needed.",
        },
        "urgency": "See a urologist within 3-5 days.",
        "doctor_type": "General Physician → Urologist",
        "foods_eat": [
            "Water — minimum 3 litres per day (most important!)",
            "Lemon juice (citrate prevents stones)",
            "Basil (Tulsi) juice — traditional kidney tonic",
            "Coconut water",
            "Cucumber, Watermelon",
            "Curd and buttermilk (for UTI)",
        ],
        "foods_avoid": [
            "Spinach, Tomatoes, Nuts (high oxalate — worsens calcium oxalate stones)",
            "Salt in excess",
            "Animal protein in excess",
            "Sugar and fructose",
            "Cold drinks and soda",
        ],
        "medicines": [
            "Antibiotics for UTI (only on prescription)",
            "Alpha blockers (help pass small stones)",
            "Pain relievers as needed",
            "Potassium citrate (prevents recurrence — doctor's advice)",
        ],
        "lifestyle": [
            "Drink water throughout the day — never let yourself feel thirsty",
            "Exercise moderately",
            "Maintain healthy weight",
            "Avoid extreme heat without hydration",
        ],
    },

    # ── THYROID ───────────────────────────────────────────────
    "Hypothyroidism (Low Thyroid)": {
        "description": (
            "Hypothyroidism means the thyroid gland is not producing enough thyroid hormone. "
            "This slows down your body's metabolism. "
            "It is very common in Indian women. Symptoms include weight gain, fatigue, "
            "cold intolerance, hair loss, and depression."
        ),
        "severity_info": {
            "Mild":     "Subclinical hypothyroidism — monitor and retest.",
            "Moderate": "Clinical hypothyroidism — medication needed.",
            "Severe":   "Severely low thyroid — requires immediate treatment.",
        },
        "urgency": "See an endocrinologist within 1 week.",
        "doctor_type": "General Physician → Endocrinologist",
        "foods_eat": [
            "Iodine-rich foods (Iodized salt, Seaweed, Fish)",
            "Selenium-rich foods (Brazil nuts, Sunflower seeds, Eggs)",
            "Zinc-rich foods (Pumpkin seeds, Chickpeas)",
            "Tyrosine-rich foods (Chicken, Turkey, Dairy)",
            "Coconut oil (supports thyroid function)",
            "Berries and antioxidant-rich foods",
        ],
        "foods_avoid": [
            "Raw cruciferous vegetables in excess (Cabbage, Broccoli, Cauliflower) — goitrogens",
            "Soy products in excess (interfere with thyroid hormone absorption)",
            "Gluten (if Hashimoto's thyroiditis)",
            "Processed foods",
            "Coffee with thyroid medication (reduces absorption)",
        ],
        "medicines": [
            "Levothyroxine (T4 replacement — gold standard treatment)",
            "Take on empty stomach, 30 min before breakfast",
            "Regular TSH monitoring every 6-12 weeks initially",
        ],
        "lifestyle": [
            "Exercise regularly — helps boost metabolism",
            "Take thyroid medication at same time every day",
            "Manage stress (cortisol worsens thyroid function)",
            "Regular TSH blood tests",
            "Adequate sleep",
        ],
    },

    "Hyperthyroidism (Overactive Thyroid)": {
        "description": (
            "Hyperthyroidism means the thyroid gland is producing too much thyroid hormone. "
            "This speeds up your body's metabolism. "
            "Symptoms include weight loss, rapid heartbeat, anxiety, sweating, and tremors. "
            "Common cause is Graves' disease."
        ),
        "severity_info": {
            "Mild":     "Mild hyperthyroidism — medication can control it well.",
            "Moderate": "Significant symptoms. Medical treatment needed urgently.",
            "Severe":   "Thyroid storm risk — emergency medical care.",
        },
        "urgency": "See an endocrinologist within 3-5 days.",
        "doctor_type": "Endocrinologist",
        "foods_eat": [
            "Cruciferous vegetables (Broccoli, Cabbage, Cauliflower — slow thyroid naturally)",
            "Calcium and Vitamin D rich foods (Milk, Curd, Cheese)",
            "Anti-inflammatory foods (Berries, Turmeric, Ginger)",
            "Magnesium-rich foods (Nuts, Seeds, Dark leafy greens)",
        ],
        "foods_avoid": [
            "Iodine-rich foods (Seaweed, excessive iodized salt)",
            "Caffeine (worsens heart palpitations and anxiety)",
            "Alcohol",
            "Soy products",
            "Processed and stimulant foods",
        ],
        "medicines": [
            "Methimazole / Carbimazole (antithyroid drugs — doctor only)",
            "Beta blockers (for rapid heartbeat control)",
            "Radioactive iodine therapy (for long-term control)",
            "Surgery (thyroidectomy) in severe cases",
        ],
        "lifestyle": [
            "Rest adequately — avoid overexertion",
            "Manage stress carefully",
            "Monitor heart rate regularly",
            "Avoid iodine supplements",
            "Regular thyroid function tests every 4-6 weeks",
        ],
    },

    "Diabetes (High Blood Sugar)": {
        "description": (
            "Diabetes means your blood sugar (glucose) level is persistently high. "
            "Type 2 diabetes is extremely common in India — often called the 'diabetes capital of the world'. "
            "Long-term high sugar damages kidneys, eyes, nerves, and heart."
        ),
        "severity_info": {
            "Mild":     "Pre-diabetes — fully reversible with lifestyle changes.",
            "Moderate": "Type 2 diabetes — medication + diet needed.",
            "Severe":   "Poorly controlled diabetes — risk of serious complications.",
        },
        "urgency": "See a diabetologist within 1 week.",
        "doctor_type": "General Physician → Diabetologist / Endocrinologist",
        "foods_eat": [
            "Bitter gourd (Karela) — natural blood sugar reducer",
            "Fenugreek seeds (Methi) soaked overnight",
            "Whole grains (Brown rice, Whole wheat, Oats)",
            "Green leafy vegetables",
            "Beans and lentils (low glycemic index)",
            "Cinnamon — helps insulin sensitivity",
            "Nuts (Almonds, Walnuts) in moderation",
        ],
        "foods_avoid": [
            "White rice, White bread, Maida items",
            "Sugar, Sweets, Mithai",
            "Fruit juices and sugary drinks",
            "Deep fried foods",
            "High-fat dairy",
            "Alcohol",
        ],
        "medicines": [
            "Metformin (first-line diabetes medication)",
            "Insulin (if required — doctor's decision)",
            "SGLT2 inhibitors, GLP-1 agonists (newer drugs)",
            "Regular HbA1c monitoring every 3 months",
        ],
        "lifestyle": [
            "Exercise 30-45 minutes daily — most important intervention",
            "Lose weight if overweight (even 5-10% weight loss helps greatly)",
            "Monitor blood sugar daily",
            "Eat small, frequent meals",
            "Avoid stress — cortisol raises blood sugar",
        ],
    },
}

# Merge into main DISEASE_DB
DISEASE_DB.update(EXTENDED_DISEASE_DB)