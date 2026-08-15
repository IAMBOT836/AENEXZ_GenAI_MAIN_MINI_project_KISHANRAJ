"""
SmartGen AI — Career Intelligence & Content Studio
Gemini REST API | Minimalist glassmorphism | White/Black
"""

import streamlit as st
import os, io, json, time, re

st.set_page_config(
    page_title="SmartGen AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS — Premium Minimal Glassmorphism
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #0a0a0a !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Canvas ── */
.stApp {
    background: #f8f9fa !important;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(224,228,240,0.5) 0%, transparent 55%),
        radial-gradient(ellipse at 100% 100%, rgba(228,224,240,0.4) 0%, transparent 55%) !important;
    min-height: 100vh;
}

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Layout ── */
.block-container {
    padding: 1.4rem 2.2rem 3rem 2.2rem !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.95) !important;
    backdrop-filter: blur(32px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
    border-right: 1px solid rgba(0,0,0,0.07) !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.8rem 1.4rem !important;
}
[data-testid="stSidebar"] * { color: #0a0a0a !important; }

/* ── Universal text ── */
h1,h2,h3,h4,h5,h6,p,span,label,strong,em,b,div {
    color: #0a0a0a !important;
}

/* ── Hero ── */
.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 16px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.03);
}
.hero-left h1 {
    font-size: 1.75rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.04em !important;
    margin: 0 0 0.15rem 0 !important;
    line-height: 1.1 !important;
    color: #0a0a0a !important;
}
.hero-left p {
    font-size: 0.88rem !important;
    color: #555 !important;
    margin: 0 !important;
    font-weight: 400 !important;
}
.hero-right {
    display: flex;
    gap: 1.4rem;
    align-items: center;
}
.hero-stat {
    text-align: center;
}
.hero-stat-num {
    font-size: 1.4rem;
    font-weight: 900;
    color: #0a0a0a !important;
    letter-spacing: -0.03em;
    display: block;
}
.hero-stat-label {
    font-size: 0.72rem;
    color: #777 !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.hero-divider {
    width: 1px;
    height: 36px;
    background: rgba(0,0,0,0.1);
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.9) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 14px !important;
    padding: 1.4rem 1.6rem !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.03) !important;
    margin-bottom: 1rem !important;
}

/* ── Info Panel ── */
.info-panel {
    background: rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.info-panel-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #888 !important;
    margin-bottom: 0.3rem;
}
.info-panel-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #0a0a0a !important;
    line-height: 1.5;
}

/* ── Section Header ── */
.section-header {
    font-size: 0.78rem !important;
    font-weight: 800 !important;
    color: #888 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin: 0 0 0.9rem 0 !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(0,0,0,0.07) !important;
}

/* ── Tabs (clean pill group) ── */
[data-testid="stTabs"] { margin-top: 0.2rem !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 6px !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    margin-bottom: 1.6rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
    visibility: hidden !important;
}

[data-testid="stTabs"] [data-baseweb="tab"],
[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.2rem !important;
    color: #666 !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    white-space: nowrap !important;
    letter-spacing: -0.01em !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover,
[data-testid="stTabs"] button[role="tab"]:hover {
    background: rgba(0,0,0,0.05) !important;
    color: #000 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #0a0a0a !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.18) !important;
    font-weight: 700 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] *,
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
    color: #fff !important;
}

/* ── Columns ── */
[data-testid="stHorizontalBlock"] {
    gap: 1.6rem !important;
    align-items: flex-start !important;
}
[data-testid="column"] { min-width: 0 !important; }

/* ── Widgets ── */
.stTextInput, .stSelectbox, .stNumberInput, .stSlider, .stTextArea, .stFileUploader, .stRadio {
    margin-bottom: 0.9rem !important;
}

label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] p {
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    color: #333 !important;
    margin-bottom: 0.3rem !important;
    letter-spacing: -0.01em !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,0.14) !important;
    border-radius: 8px !important;
    color: #0a0a0a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 0.8rem !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #0a0a0a !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.07) !important;
    outline: none !important;
}

/* selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,0.14) !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}

/* slider */
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: #0a0a0a !important; }

/* radio */
[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 0.8rem !important;
    margin-top: 0.25rem !important;
    flex-wrap: wrap !important;
}
[data-testid="stRadio"] label {
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}

/* ── Primary Button ── */
.stButton { margin-bottom: 0.5rem !important; }
.stButton > button {
    background: #0a0a0a !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.14) !important;
    letter-spacing: -0.01em !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button * { color: #fff !important; }
.stButton > button:hover {
    background: #222 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Secondary / Ghost Button ── */
.stButton > button[kind="secondary"] {
    background: #fff !important;
    color: #0a0a0a !important;
    border: 1px solid rgba(0,0,0,0.18) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
.stButton > button[kind="secondary"] * { color: #0a0a0a !important; }
.stButton > button[kind="secondary"]:hover {
    background: #f5f5f5 !important;
    border-color: #0a0a0a !important;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] { margin-bottom: 0.5rem !important; }
[data-testid="stDownloadButton"] button {
    background: #fff !important;
    color: #0a0a0a !important;
    border: 1px solid rgba(0,0,0,0.16) !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.18s !important;
}
[data-testid="stDownloadButton"] button * { color: #0a0a0a !important; }
[data-testid="stDownloadButton"] button:hover {
    border-color: #0a0a0a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
}

/* ── Output Box ── */
.output-box {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 10px !important;
    padding: 1.2rem 1.4rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.81rem !important;
    color: #0a0a0a !important;
    line-height: 1.75 !important;
    min-height: 260px !important;
    max-height: 540px !important;
    overflow-y: auto !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.02) !important;
    margin-bottom: 0.6rem !important;
}
.output-box::-webkit-scrollbar { width: 5px; }
.output-box::-webkit-scrollbar-track { background: rgba(0,0,0,0.02); border-radius: 3px; }
.output-box::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 3px; }

/* ── Chips ── */
.chip {
    display: inline-block;
    background: rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.09);
    border-radius: 20px;
    padding: 0.18rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #0a0a0a !important;
    margin: 2px;
}
.chip-match {
    background: rgba(0,0,0,0.05);
    border-color: rgba(0,0,0,0.15);
    color: #0a0a0a !important;
}
.chip-miss {
    background: rgba(200,30,30,0.06);
    border-color: rgba(200,30,30,0.2);
    color: #7f1d1d !important;
}
.chip-meta {
    background: rgba(0,0,0,0.03);
    border-color: rgba(0,0,0,0.06);
    color: #555 !important;
}

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #0a0a0a;
    color: #fff !important;
    font-size: 1.4rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    min-width: 88px;
}
.score-badge.good { background: #0a0a0a; }
.score-badge.warn { background: #92400e; }
.score-badge.low  { background: #7f1d1d; }

/* ── Stat row inside profile ── */
.stat-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin: 0.8rem 0;
}
.stat-item {
    background: rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    flex: 1;
    min-width: 80px;
    text-align: center;
}
.stat-item-num {
    font-size: 1.1rem;
    font-weight: 900;
    color: #0a0a0a !important;
    letter-spacing: -0.02em;
    display: block;
}
.stat-item-label {
    font-size: 0.7rem;
    color: #777 !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: block;
}

/* ── Sidebar stat ── */
.sidebar-stat {
    background: rgba(0,0,0,0.025);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 8px;
    padding: 0.55rem 0.85rem;
    margin-bottom: 0.35rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.sidebar-stat-label { font-size: 0.8rem; color: #555 !important; font-weight: 500; }
.sidebar-stat-value { font-size: 0.85rem; font-weight: 800; color: #0a0a0a !important; }

/* ── Status pill ── */
.pill {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 700;
}
.pill-active { background: rgba(0,0,0,0.08); border: 1px solid rgba(0,0,0,0.15); color: #0a0a0a !important; }
.pill-idle { background: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.08); color: #777 !important; }

/* ── Chat ── */
.chat-wrap { display: flex; flex-direction: column; gap: 0.7rem; margin-bottom: 1rem; }
.bubble-user {
    background: #0a0a0a;
    color: #fff !important;
    padding: 0.85rem 1.1rem;
    border-radius: 14px 14px 4px 14px;
    max-width: 78%;
    align-self: flex-end;
    font-size: 0.88rem;
    line-height: 1.55;
    font-weight: 500;
}
.bubble-user * { color: #fff !important; }
.bubble-ai {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(0,0,0,0.08);
    color: #0a0a0a !important;
    padding: 1rem 1.2rem;
    border-radius: 14px 14px 14px 4px;
    max-width: 88%;
    align-self: flex-start;
    font-size: 0.88rem;
    line-height: 1.65;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.bubble-ai * { color: #0a0a0a !important; }

/* ── Quick prompt button strip ── */
.prompt-btn { margin-bottom: 0.4rem !important; }
.prompt-btn .stButton > button {
    background: rgba(0,0,0,0.04) !important;
    color: #0a0a0a !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    box-shadow: none !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
}
.prompt-btn .stButton > button:hover {
    background: rgba(0,0,0,0.08) !important;
    border-color: rgba(0,0,0,0.2) !important;
    transform: none !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px dashed rgba(0,0,0,0.16) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,0,0,0.35) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.88) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: 0.86rem !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(0,0,0,0.09) !important;
    border-radius: 10px !important;
    font-size: 0.86rem !important;
}
[data-testid="stAlert"] * { font-size: 0.86rem !important; }

/* ── Divider ── */
hr {
    margin: 1rem 0 !important;
    border: none !important;
    border-top: 1px solid rgba(0,0,0,0.07) !important;
}

/* ── Match job card ── */
.job-card {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.job-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-color: rgba(0,0,0,0.15);
}
.job-title { font-size: 1rem; font-weight: 800; color: #0a0a0a !important; margin-bottom: 0.15rem; }
.job-meta { font-size: 0.8rem; color: #555 !important; font-weight: 500; margin-bottom: 0.5rem; }
.job-summary { font-size: 0.82rem; color: #333 !important; line-height: 1.5; margin-bottom: 0.6rem; }

/* ── Spinner and success ── */
.stSpinner { opacity: 0.7; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def extract_text_from_file(uploaded_file) -> str:
    filename = uploaded_file.name.lower()
    try:
        if filename.endswith(".pdf"):
            import pypdf
            reader = pypdf.PdfReader(uploaded_file)
            return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        elif filename.endswith(".docx"):
            import docx
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()
        else:
            raw = uploaded_file.read()
            return raw.decode("utf-8", errors="replace").strip()
    except Exception as e:
        raise ValueError(f"Could not read {filename}: {e}")


def call_gemini(system: str, prompt: str, temp: float, api_key: str, model: str = "gemini-2.0-flash") -> str:
    import requests
    if not api_key or not api_key.strip():
        raise ValueError("API key missing.")
    candidates = [model, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]
    seen, tried = set(), []
    errors = []
    for m in candidates:
        if m in seen: continue
        seen.add(m)
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key.strip()}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "systemInstruction": {"parts": [{"text": system}]},
                "generationConfig": {"temperature": temp},
            }
            r = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=60)
            if r.status_code == 200:
                data = r.json()
                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
                errors.append(f"{m}: empty response")
            else:
                try: msg = r.json().get("error", {}).get("message", r.text[:120])
                except: msg = r.text[:120]
                errors.append(f"{m} ({r.status_code}): {msg}")
        except Exception as e:
            errors.append(f"{m}: {e}")
    raise RuntimeError("All models failed:\n" + "\n".join(errors[-4:]))


def parse_resume_ai(text: str, api_key: str, model: str) -> dict:
    system = "Expert Resume Parser and ATS Auditor. Return ONLY valid JSON, no markdown."
    prompt = f"""Parse this resume into structured JSON.

Resume:
\"\"\"{text[:5500]}\"\"\"

Return ONLY this JSON:
{{
  "name": "Full Name",
  "target_role": "Target Role",
  "contact": {{"email":"","phone":"","location":""}},
  "ats_score": 82,
  "summary": "3-sentence summary.",
  "skills": {{"technical":["Skill1"],"tools":["Tool1"],"soft":["Skill1"]}},
  "experience": [{{"role":"","company":"","duration":"","highlights":["Achievement"]}}],
  "education": [{{"degree":"","institution":"","year":""}}],
  "certifications": [],
  "ats_improvements": ["Tip 1","Tip 2"]
}}"""
    raw = call_gemini(system, prompt, 0.1, api_key, model)
    clean = raw
    if "```json" in clean: clean = clean.split("```json")[1].split("```")[0].strip()
    elif "```" in clean: clean = clean.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(clean)
    except:
        return {
            "name": "Candidate", "target_role": "Professional",
            "contact": {"email": "N/A", "phone": "N/A", "location": "N/A"},
            "ats_score": 75, "summary": clean[:250],
            "skills": {"technical": ["Python"], "tools": ["Git"], "soft": ["Communication"]},
            "experience": [{"role": "Experience", "company": "Company", "duration": "Recent", "highlights": [clean[:150]]}],
            "education": [{"degree": "Degree", "institution": "University", "year": "Recent"}],
            "certifications": [], "ats_improvements": ["Add metrics to achievements."]
        }


JOB_CORPUS = [
    {"id": "j1", "title": "Generative AI Engineer", "company": "AI Labs", "domain": "AI / ML",
     "skills": ["Python","LLMs","RAG","Gemini API","Prompt Engineering","Vector DB","FastAPI","Docker"],
     "desc": "Build production RAG systems, integrate LLM APIs, and deploy intelligent AI applications at scale."},
    {"id": "j2", "title": "Full Stack Developer", "company": "CloudScale", "domain": "Web Engineering",
     "skills": ["Python","React","TypeScript","FastAPI","PostgreSQL","REST APIs","Docker","Git"],
     "desc": "Design responsive applications, build high-performance APIs, and lead end-to-end product development."},
    {"id": "j3", "title": "Data Scientist", "company": "Apex Analytics", "domain": "Data Science",
     "skills": ["Python","SQL","Pandas","Scikit-Learn","TensorFlow","Statistics","Machine Learning","Spark"],
     "desc": "Analyze large datasets, develop predictive models, and produce actionable business insights."},
    {"id": "j4", "title": "Cloud & DevOps Architect", "company": "Nebula Cloud", "domain": "Infrastructure",
     "skills": ["AWS","Docker","Kubernetes","CI/CD","Terraform","Linux","Python","Monitoring","IaC"],
     "desc": "Design resilient cloud infrastructure, automate deployments, and implement observability."},
    {"id": "j5", "title": "Frontend Engineer", "company": "Interface Labs", "domain": "Frontend",
     "skills": ["React","Next.js","JavaScript","TypeScript","CSS","UI/UX","REST APIs","Git","Figma"],
     "desc": "Craft performant, accessible web experiences with modern frameworks and design systems."},
]


def match_jobs(profile: dict, jobs: list, api_key: str, model: str) -> list:
    p_summary = f"Role: {profile.get('target_role')}\nSkills: {json.dumps(profile.get('skills',{}))}\nSummary: {profile.get('summary','')}"
    j_list = json.dumps([{"id": j["id"], "title": j["title"], "skills": j.get("skills", j.get("skills_required", []))} for j in jobs])
    system = "AI Talent Matcher. Return ONLY a JSON array."
    prompt = f"""Candidate:
{p_summary}

Jobs:
{j_list}

Return JSON array only:
[{{"id":"j1","match_score":85,"matched_skills":["Skill"],"missing_skills":["Skill"],"fit_summary":"One sentence."}}]"""
    raw = call_gemini(system, prompt, 0.1, api_key, model)
    clean = raw
    if "```json" in clean: clean = clean.split("```json")[1].split("```")[0].strip()
    elif "```" in clean: clean = clean.split("```")[1].split("```")[0].strip()
    try: score_map = {s["id"]: s for s in json.loads(clean)}
    except: score_map = {}
    results = []
    for j in jobs:
        jid = j["id"]
        j_skills = j.get("skills", j.get("skills_required", []))
        if jid in score_map:
            results.append({**j, **score_map[jid]})
        else:
            c_skills = set(s.lower() for cat in profile.get("skills", {}).values() for s in cat)
            matched = [s for s in j_skills if s.lower() in c_skills]
            missing = [s for s in j_skills if s.lower() not in c_skills]
            score = int(len(matched) / max(len(j_skills), 1) * 100)
            results.append({**j, "match_score": score, "matched_skills": matched,
                             "missing_skills": missing, "fit_summary": f"Matches {len(matched)}/{len(j_skills)} requirements."})
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return results


def generate_cv_suggestions(profile: dict, job: dict, api_key: str, model: str) -> str:
    j_skills = job.get("skills", job.get("skills_required", []))
    system = "Executive Resume Strategist and Career Coach. Write actionable, high-impact CV optimization."
    prompt = f"""Candidate Profile:
{json.dumps(profile, indent=2)}

Target: {job.get('title')} at {job.get('company')}
Required Skills: {', '.join(j_skills)}
Description: {job.get('desc', job.get('description', ''))}

Structure your response clearly:

1. TARGETED PROFESSIONAL SUMMARY
Write a polished 3-4 sentence summary tailored to this role.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. MISSING KEYWORDS & SKILLS
List exact ATS keywords missing from the candidate's profile.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. BULLET POINT REWRITES (XYZ Format)
Rewrite 3 experience bullets using:
"Accomplished [X] as measured by [Y], by doing [Z]"
Format:
  Before: [original bullet]
  After:  [improved bullet]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. ATS AUDIT & COMPLIANCE
3 specific actions to maximize ATS parsing and interview callback rate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. TAILORED RESUME DRAFT
Full resume preview in clean text format.
"""
    return call_gemini(system, prompt, 0.3, api_key, model)


def mentor_chat(messages: list, profile_ctx: str, job_ctx: str, api_key: str, model: str) -> str:
    system = f"""You are SmartGen Career Mentor — an elite executive career advisor, interview coach, and talent strategist.

Candidate Context: {profile_ctx}
Target Role Context: {job_ctx}

Provide direct, actionable coaching without emojis. Use clear structure and formatting.
"""
    history = "\n\n".join(f"{'User' if m['role'] == 'user' else 'Advisor'}: {m['content']}" for m in messages)
    prompt = f"Conversation:\n{history}\n\nRespond to the user's latest message with structured, actionable guidance."
    return call_gemini(system, prompt, 0.5, api_key, model)


def generate_blog(topic: str, tone: str, words: int, api_key: str, model: str) -> str:
    system = "Experienced professional writer crafting clear, insightful, well-structured articles."
    prompt = f"""Write an article:
Topic: "{topic}"
Tone: {tone}
Target words: ~{words}

Structure:
1. Title (compelling, clean)
2. Introduction (strong hook)
3. 2-3 body sections with subheadings
4. Conclusion with clear takeaway

Write in full paragraphs. No emojis."""
    return call_gemini(system, prompt, 0.7, api_key, model)


def generate_email(recipient: str, purpose: str, tone: str, api_key: str, model: str) -> str:
    system = "Professional communication specialist drafting polished, concise business emails."
    prompt = f"""Write a professional email:
Recipient: {recipient}
Purpose: {purpose}
Tone: {tone}

Format:
Subject: [subject line]

[Salutation],

[Body — clear and concise]

[Professional sign-off],
[Sender Name]
[Contact Details]"""
    return call_gemini(system, prompt, 0.3, api_key, model)


def generate_resume(name, title, email, phone, location, summary, experience, education, skills, projects, certs, api_key, model) -> str:
    system = "Expert ATS resume writer. Use strong action verbs and quantified achievements."
    prompt = f"""Build a professional ATS resume:

Name: {name}
Target Role: {title}
Email: {email} | Phone: {phone} | Location: {location}

Summary Notes: {summary}
Experience: {experience}
Education: {education}
Skills: {skills}
Projects: {projects}
Certifications: {certs}

Format rules:
- Use ━━━ as section dividers
- Experience: reverse-chronological bullet points with metrics
- Skills: grouped by category
- Output plain text only, 1-2 page length
"""
    return call_gemini(system, prompt, 0.2, api_key, model)


# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────
for k, v in {
    "blog_history": [], "email_history": [], "resume_history": [],
    "parsed_profile": None, "selected_job": None, "cv_output": None,
    "matched_jobs": None,
    "mentor_messages": [{"role": "assistant", "content": "Hello. I am your Career Advisor. Upload a resume or select a target role to begin — I can help with interview preparation, learning roadmaps, or cover letter drafting."}],
    "total_ops": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom:1.4rem; border-bottom:1px solid rgba(0,0,0,0.07); margin-bottom:1.2rem;">
        <div style="font-size:1.1rem;font-weight:900;color:#0a0a0a;letter-spacing:-0.03em;">SmartGen AI</div>
        <div style="font-size:0.75rem;color:#777;margin-top:0.15rem;font-weight:500;">Career Intelligence & Content Studio</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#888;margin-bottom:0.5rem;">Configuration</div>', unsafe_allow_html=True)

    default_key = ""
    try:
        if "GEMINI_API_KEY" in st.secrets: default_key = st.secrets["GEMINI_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets: default_key = st.secrets["GOOGLE_API_KEY"]
    except: pass
    if not default_key:
        default_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")

    api_key = st.text_input("Gemini API Key", type="password", value=default_key, placeholder="Enter API key…")
    model_choice = st.selectbox("Model", ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-3.5-flash"], index=0)

    if api_key:
        st.markdown('<div class="pill pill-active" style="margin-top:-0.2rem;margin-bottom:0.8rem;">Key Active</div>', unsafe_allow_html=True)
    else:
        st.caption("Enter API key to enable generation.")

    st.markdown('<hr style="margin:1rem 0 0.9rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#888;margin-bottom:0.6rem;">Session</div>', unsafe_allow_html=True)

    has_profile = "Active" if st.session_state.parsed_profile else "None"
    target = st.session_state.selected_job.get("title", "None")[:22] if st.session_state.selected_job else "None"
    st.markdown(f"""
    <div class="sidebar-stat"><span class="sidebar-stat-label">Profile</span><span class="sidebar-stat-value">{has_profile}</span></div>
    <div class="sidebar-stat"><span class="sidebar-stat-label">Target</span><span class="sidebar-stat-value">{target}</span></div>
    <div class="sidebar-stat"><span class="sidebar-stat-label">Articles</span><span class="sidebar-stat-value">{len(st.session_state.blog_history)}</span></div>
    <div class="sidebar-stat"><span class="sidebar-stat-label">Emails</span><span class="sidebar-stat-value">{len(st.session_state.email_history)}</span></div>
    <div class="sidebar-stat"><span class="sidebar-stat-label">Resumes</span><span class="sidebar-stat-value">{len(st.session_state.resume_history)}</span></div>
    <div class="sidebar-stat"><span class="sidebar-stat-label">Operations</span><span class="sidebar-stat-value">{st.session_state.total_ops}</span></div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:1rem 0 0.9rem 0;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.75rem;color:#999;line-height:1.7;">
        Powered by Google Gemini REST API.<br>
        Parser → Matcher → Optimizer → Mentor
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────────────────────
total_blog = len(st.session_state.blog_history)
total_email = len(st.session_state.email_history)
total_resume = len(st.session_state.resume_history)
profile_status = "Loaded" if st.session_state.parsed_profile else "None"

st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <h1>SmartGen AI</h1>
        <p>Career Intelligence &amp; Content Studio — Powered by Gemini</p>
    </div>
    <div class="hero-right">
        <div class="hero-stat">
            <span class="hero-stat-num">{st.session_state.total_ops}</span>
            <span class="hero-stat-label">Operations</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-stat">
            <span class="hero-stat-num">{total_blog + total_email + total_resume}</span>
            <span class="hero-stat-label">Generated</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-stat">
            <span class="hero-stat-num">{profile_status}</span>
            <span class="hero-stat-label">Profile</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Navigation
# ─────────────────────────────────────────────────────────────
tab_career, tab_blog, tab_email, tab_resume, tab_history = st.tabs([
    "Career Intelligence",
    "Blog Studio",
    "Email Writer",
    "Resume Builder",
    "History",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — CAREER INTELLIGENCE
# ══════════════════════════════════════════════════════════════
with tab_career:
    step = st.radio(
        "Step:",
        ["1  —  Resume Parser", "2  —  Job Matching", "3  —  CV Optimizer", "4  —  Career Mentor"],
        horizontal=True,
        key="career_step",
        label_visibility="collapsed",
    )
    st.markdown('<hr style="margin:0.6rem 0 1.2rem 0;">', unsafe_allow_html=True)

    # ── STEP 1 ─────────────────────────────────────────────────
    if "1" in step:
        col_l, col_r = st.columns([1, 1.1], gap="large")

        with col_l:
            st.markdown('<div class="section-header">Resume Input</div>', unsafe_allow_html=True)

            input_mode = st.radio("Method", ["Upload file", "Paste text"], horizontal=True, key="resume_input_mode")
            resume_text = ""

            if input_mode == "Upload file":
                uf = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], label_visibility="collapsed")
                if uf:
                    try:
                        resume_text = extract_text_from_file(uf)
                        st.success(f"Extracted {len(resume_text.split())} words from **{uf.name}**")
                        with st.expander("Preview extracted text"):
                            st.text(resume_text[:1500] + ("…" if len(resume_text) > 1500 else ""))
                    except Exception as e:
                        st.error(str(e))
            else:
                resume_text = st.text_area("Paste resume content", placeholder="Paste your full resume text here…", height=260, label_visibility="collapsed")

            parse_btn = st.button("Analyze Resume", use_container_width=True, key="parse_btn")

            if parse_btn:
                if not api_key:
                    st.error("Enter your Gemini API key in the sidebar.")
                elif not resume_text.strip():
                    st.warning("Provide resume content — upload a file or paste text.")
                else:
                    with st.spinner("Parsing resume and computing ATS score…"):
                        try:
                            t = time.time()
                            st.session_state.parsed_profile = parse_resume_ai(resume_text, api_key, model_choice)
                            st.session_state.total_ops += 1
                            st.success(f"Parsed in {round(time.time()-t,1)}s — navigate to Step 2 to match jobs.")
                        except Exception as e:
                            st.error(str(e))

        with col_r:
            st.markdown('<div class="section-header">Candidate Profile</div>', unsafe_allow_html=True)
            p = st.session_state.parsed_profile
            if p:
                ats = p.get("ats_score", 80)
                badge_cls = "good" if ats >= 80 else "warn" if ats >= 60 else "low"
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"""
                    <div style="text-align:center;padding:1rem;background:rgba(0,0,0,0.03);border-radius:12px;border:1px solid rgba(0,0,0,0.07);">
                        <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#888;margin-bottom:0.4rem;">ATS Score</div>
                        <div class="score-badge {badge_cls}">{ats}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    name = p.get("name", "Candidate")
                    role = p.get("target_role", "")
                    loc = p.get("contact", {}).get("location", "N/A")
                    email_c = p.get("contact", {}).get("email", "N/A")
                    st.markdown(f"""
                    <div style="padding:0.2rem 0;">
                        <div style="font-size:1.15rem;font-weight:900;color:#0a0a0a;letter-spacing:-0.02em;">{name}</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#333;margin-top:0.1rem;">{role}</div>
                        <div style="font-size:0.78rem;color:#666;margin-top:0.3rem;">{loc} · {email_c}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)

                # Summary
                if p.get("summary"):
                    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#888;margin-bottom:0.4rem;">Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:0.86rem;color:#222;line-height:1.65;background:rgba(0,0,0,0.02);padding:0.8rem 1rem;border-radius:8px;border:1px solid rgba(0,0,0,0.06);">{p["summary"]}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # Skills
                skills = p.get("skills", {})
                if skills:
                    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#888;margin-bottom:0.5rem;">Skills</div>', unsafe_allow_html=True)
                    for cat, items in skills.items():
                        if not items: continue
                        label = cat.replace("_", " ").title()
                        chips = "".join(f'<span class="chip">{s}</span>' for s in items)
                        st.markdown(f'<div style="margin-bottom:0.5rem;"><span style="font-size:0.74rem;font-weight:700;color:#555;">{label}: </span>{chips}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # Experience
                exp_list = p.get("experience", [])
                if exp_list:
                    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#888;margin-bottom:0.5rem;">Experience</div>', unsafe_allow_html=True)
                    for exp in exp_list:
                        label = f"{exp.get('role','Role')} — {exp.get('company','Company')} ({exp.get('duration','Dates')})"
                        with st.expander(label):
                            for h in exp.get("highlights", []):
                                st.markdown(f"- {h}")

                # ATS Tips
                tips = p.get("ats_improvements", [])
                if tips:
                    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#888;margin:0.6rem 0 0.4rem;">ATS Recommendations</div>', unsafe_allow_html=True)
                    for tip in tips:
                        st.markdown(f'<div style="font-size:0.83rem;padding:0.4rem 0.7rem;background:rgba(0,0,0,0.025);border-left:2px solid rgba(0,0,0,0.15);border-radius:0 6px 6px 0;margin-bottom:0.3rem;color:#333;">↳ {tip}</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:center;padding:5rem 2rem;color:#aaa;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;opacity:0.3;">↑</div>
                    <div style="font-size:0.9rem;font-weight:600;color:#888;">No profile loaded</div>
                    <div style="font-size:0.8rem;margin-top:0.25rem;color:#aaa;">Upload or paste your resume on the left</div>
                </div>
                """, unsafe_allow_html=True)

    # ── STEP 2 ─────────────────────────────────────────────────
    elif "2" in step:
        st.markdown('<div class="section-header">Job Matching & Skill Gap Analysis</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("Parse your resume in Step 1 first.")
        else:
            col_l, col_r = st.columns([1, 1.8], gap="large")

            with col_l:
                st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#555;margin-bottom:0.6rem;">Job Source</div>', unsafe_allow_html=True)
                src = st.radio("Source", ["Built-in Corpus", "Custom Job Description"], key="job_src", label_visibility="collapsed")

                active_jobs = list(JOB_CORPUS)
                if src == "Custom Job Description":
                    st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)
                    c_title = st.text_input("Job Title", placeholder="e.g. AI Engineer", key="cj_title")
                    c_co = st.text_input("Company", placeholder="e.g. FAANG Corp", key="cj_co")
                    c_sk = st.text_input("Required Skills (comma-separated)", placeholder="Python, LLMs, FastAPI…", key="cj_sk")
                    c_desc = st.text_area("Job Description", placeholder="Paste the full JD here…", height=120, key="cj_desc")
                    if c_title:
                        active_jobs = [{"id": "cj0", "title": c_title, "company": c_co or "Company",
                                        "domain": "Custom", "skills": [s.strip() for s in c_sk.split(",") if s.strip()],
                                        "desc": c_desc}] + JOB_CORPUS

                if st.button("Match Positions", use_container_width=True, key="match_btn"):
                    if not api_key:
                        st.error("Enter API key.")
                    else:
                        with st.spinner("Computing semantic match scores…"):
                            try:
                                t = time.time()
                                st.session_state.matched_jobs = match_jobs(st.session_state.parsed_profile, active_jobs, api_key, model_choice)
                                st.session_state.total_ops += 1
                                st.success(f"Matched {len(active_jobs)} positions in {round(time.time()-t,1)}s.")
                            except Exception as e:
                                st.error(str(e))

            with col_r:
                st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#555;margin-bottom:0.6rem;">Ranked Results</div>', unsafe_allow_html=True)
                matched = st.session_state.matched_jobs
                if matched:
                    for i, job in enumerate(matched):
                        score = job.get("match_score", 0)
                        badge_cls = "good" if score >= 80 else "warn" if score >= 60 else "low"
                        j_skills = job.get("skills", job.get("skills_required", []))
                        matched_s = job.get("matched_skills", [])
                        missing_s = job.get("missing_skills", [])
                        fit = job.get("fit_summary", job.get("desc", "")[:120])

                        st.markdown(f"""
                        <div class="job-card">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
                                <div>
                                    <div class="job-title">{job.get('title','')}</div>
                                    <div class="job-meta">{job.get('company','')} · {job.get('domain','')}</div>
                                    <div class="job-summary">{fit}</div>
                                </div>
                                <div style="flex-shrink:0;">
                                    <span class="score-badge {badge_cls}" style="font-size:1rem;padding:0.45rem 0.9rem;">{score}%</span>
                                </div>
                            </div>
                            <div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.2rem;">
                                {"".join(f'<span class="chip chip-match">{s}</span>' for s in matched_s[:6])}
                                {"".join(f'<span class="chip chip-miss">{s}</span>' for s in missing_s[:4])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"Select — {job.get('title','')[:28]}", key=f"sel_{job['id']}_{i}", use_container_width=False):
                            st.session_state.selected_job = job
                            st.success(f"Target set: {job.get('title')} — proceed to Step 3.")

                        if i < len(matched) - 1:
                            st.markdown('<hr style="margin:0 0 0.2rem 0;">', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align:center;padding:3rem 2rem;color:#aaa;">
                        <div style="font-size:0.9rem;font-weight:600;color:#888;">No matches yet</div>
                        <div style="font-size:0.8rem;margin-top:0.2rem;">Click Match Positions to score your profile.</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── STEP 3 ─────────────────────────────────────────────────
    elif "3" in step:
        st.markdown('<div class="section-header">CV Optimization & Bullet Rewriter</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("Parse resume in Step 1 first.")
        else:
            col_l, col_r = st.columns([1, 1.5], gap="large")

            with col_l:
                st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#555;margin-bottom:0.6rem;">Target Position</div>', unsafe_allow_html=True)

                job_opts = [f"{j['title']} — {j['company']}" for j in JOB_CORPUS]
                sel_idx = 0
                if st.session_state.selected_job:
                    cur = st.session_state.selected_job.get("title", "")
                    for i, o in enumerate(job_opts):
                        if cur in o: sel_idx = i; break

                chosen = st.selectbox("Position", job_opts, index=sel_idx, label_visibility="collapsed")
                target_job = JOB_CORPUS[0]
                for j in JOB_CORPUS:
                    if j["title"] in chosen:
                        target_job = j
                        break
                if st.session_state.selected_job:
                    target_job = st.session_state.selected_job

                j_skills = target_job.get("skills", target_job.get("skills_required", []))
                st.markdown(f"""
                <div class="info-panel">
                    <div class="info-panel-label">Selected Role</div>
                    <div class="info-panel-value" style="font-size:0.95rem;font-weight:800;">{target_job.get('title','')}</div>
                    <div style="font-size:0.8rem;color:#555;margin-top:0.15rem;">{target_job.get('company','')}</div>
                    <div style="margin-top:0.6rem;">{"".join(f'<span class="chip chip-meta">{s}</span>' for s in j_skills[:8])}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Generate Optimization Plan", use_container_width=True, key="cv_btn"):
                    if not api_key:
                        st.error("Enter API key.")
                    else:
                        with st.spinner("Generating XYZ bullet rewrites and keyword recommendations…"):
                            try:
                                t = time.time()
                                st.session_state.cv_output = generate_cv_suggestions(st.session_state.parsed_profile, target_job, api_key, model_choice)
                                st.session_state.total_ops += 1
                                st.success(f"Generated in {round(time.time()-t,1)}s.")
                            except Exception as e:
                                st.error(str(e))

            with col_r:
                st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#555;margin-bottom:0.6rem;">Optimization Plan</div>', unsafe_allow_html=True)
                if st.session_state.cv_output:
                    st.markdown(f'<div class="output-box">{st.session_state.cv_output}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "Download Plan (.txt)",
                        data=st.session_state.cv_output,
                        file_name=f"CV_Plan_{target_job.get('title','').replace(' ','_')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                else:
                    st.markdown("""
                    <div style="text-align:center;padding:5rem 2rem;color:#aaa;border:1.5px dashed rgba(0,0,0,0.1);border-radius:12px;">
                        <div style="font-size:0.9rem;font-weight:600;color:#888;">Optimization Plan</div>
                        <div style="font-size:0.8rem;margin-top:0.2rem;">Select a target role and click Generate.</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── STEP 4 ─────────────────────────────────────────────────
    elif "4" in step:
        st.markdown('<div class="section-header">Career Mentor</div>', unsafe_allow_html=True)

        col_l, col_r = st.columns([0.85, 2], gap="large")

        with col_l:
            p = st.session_state.parsed_profile
            j = st.session_state.selected_job
            profile_ctx = f"Candidate: {p.get('name')} | Role: {p.get('target_role')} | Skills: {json.dumps(p.get('skills',{}))}" if p else "No resume uploaded"
            job_ctx = f"Target: {j.get('title')} at {j.get('company')} | Required: {j.get('skills', j.get('skills_required', []))}" if j else "General industry"

            st.markdown(f"""
            <div class="info-panel" style="margin-bottom:0.8rem;">
                <div class="info-panel-label">Profile Context</div>
                <div class="info-panel-value">{profile_ctx[:100]}…</div>
            </div>
            <div class="info-panel">
                <div class="info-panel-label">Target Role</div>
                <div class="info-panel-value">{job_ctx[:100]}…</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#888;margin:0.8rem 0 0.5rem;">Quick Prompts</div>', unsafe_allow_html=True)

            prompts = {
                "Mock Interview Questions": "Generate 5 challenging interview questions tailored to my resume and target role, with detailed STAR method answer frameworks for each.",
                "60-Day Learning Plan": "Create a structured 60-day step-by-step learning roadmap with weekly milestones to bridge my skill gaps for this target role.",
                "Draft Cover Letter": "Write a professional cover letter for this position highlighting my most relevant experience and achievements. Keep it under 300 words.",
                "Salary Strategy": "Provide a data-driven salary negotiation strategy and script for this role, including market benchmarks and negotiation tactics.",
            }
            auto_prompt = None
            for label, prompt_text in prompts.items():
                with st.container():
                    if st.button(label, use_container_width=True, key=f"qp_{label[:8]}"):
                        auto_prompt = prompt_text

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear Conversation", use_container_width=True, key="clear_chat", type="secondary"):
                st.session_state.mentor_messages = [{"role": "assistant", "content": "Conversation cleared. How can I help?"}]
                st.rerun()

        with col_r:
            # Render chat history
            chat_html = '<div class="chat-wrap">'
            for msg in st.session_state.mentor_messages:
                cls = "bubble-user" if msg["role"] == "user" else "bubble-ai"
                chat_html += f'<div class="{cls}">{msg["content"]}</div>'
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            user_input = st.chat_input("Ask about interview prep, skill gaps, cover letters, or career strategy…")
            final_input = auto_prompt or user_input

            if final_input:
                if not api_key:
                    st.error("Enter API key.")
                else:
                    st.session_state.mentor_messages.append({"role": "user", "content": final_input})
                    with st.spinner("Thinking…"):
                        try:
                            reply = mentor_chat(st.session_state.mentor_messages, profile_ctx, job_ctx, api_key, model_choice)
                            st.session_state.mentor_messages.append({"role": "assistant", "content": reply})
                            st.session_state.total_ops += 1
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))


# ══════════════════════════════════════════════════════════════
# TAB 2 — BLOG STUDIO
# ══════════════════════════════════════════════════════════════
with tab_blog:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown('<div class="section-header">Article Parameters</div>', unsafe_allow_html=True)

        topic = st.text_input("Topic", placeholder="e.g. The Future of AI in Healthcare", value="The Future of AI in Healthcare")
        tone = st.selectbox("Writing Tone", ["professional", "analytical", "executive", "formal", "conversational"])
        words = st.slider("Target Word Count", 100, 1500, 400, 50)

        st.markdown(f"""
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:-0.2rem 0 0.8rem;">
            <span class="chip chip-meta">Tone: {tone}</span>
            <span class="chip chip-meta">~{words} words</span>
            <span class="chip chip-meta">Temp: 0.7</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Article", use_container_width=True, key="gen_blog"):
            if not api_key: st.error("Enter API key.")
            elif not topic.strip(): st.warning("Enter a topic.")
            else:
                with st.spinner("Writing article…"):
                    try:
                        t = time.time()
                        out = generate_blog(topic, tone, words, api_key, model_choice)
                        header = f"--- ARTICLE ---\nTopic: {topic}\nTone: {tone}\nWords: ~{words}\n\n"
                        full = header + out
                        st.session_state.blog_history.append({"topic": topic, "tone": tone, "words": words, "output": full})
                        st.session_state.total_ops += 1
                        st.success(f"Generated in {round(time.time()-t,1)}s.")
                    except Exception as e:
                        st.error(str(e))

    with col_r:
        st.markdown('<div class="section-header">Generated Article</div>', unsafe_allow_html=True)
        if st.session_state.blog_history:
            last = st.session_state.blog_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button("Download Article (.txt)", data=last["output"], file_name="article.txt", mime="text/plain", use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:5rem 2rem;color:#aaa;border:1.5px dashed rgba(0,0,0,0.1);border-radius:12px;">
                <div style="font-size:0.9rem;font-weight:600;color:#888;">No article yet</div>
                <div style="font-size:0.8rem;margin-top:0.2rem;">Configure parameters and click Generate.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — EMAIL WRITER
# ══════════════════════════════════════════════════════════════
with tab_email:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown('<div class="section-header">Email Parameters</div>', unsafe_allow_html=True)

        recipient = st.text_input("Recipient", placeholder="e.g. Hiring Manager, FAANG Corp", value="Hiring Manager")
        purpose = st.selectbox("Purpose", [
            "Interview Follow-up", "Cold Outreach", "Thank-You Note",
            "Meeting Request", "Offer Negotiation", "Status Update", "Custom"
        ])
        if purpose == "Custom":
            purpose = st.text_input("Describe the purpose", placeholder="e.g. Request project extension…")

        email_tone = st.selectbox("Tone", ["professional", "formal", "concise", "assertive", "warm"])

        st.markdown(f"""
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:-0.2rem 0 0.8rem;">
            <span class="chip chip-meta">Tone: {email_tone}</span>
            <span class="chip chip-meta">Temp: 0.3</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Compose Email", use_container_width=True, key="gen_email"):
            if not api_key: st.error("Enter API key.")
            elif not recipient.strip(): st.warning("Enter recipient.")
            elif not purpose or not purpose.strip(): st.warning("Enter purpose.")
            else:
                with st.spinner("Composing email…"):
                    try:
                        t = time.time()
                        out = generate_email(recipient, purpose, email_tone, api_key, model_choice)
                        header = f"--- EMAIL ---\nTo: {recipient}\nPurpose: {purpose}\nTone: {email_tone}\n\n"
                        full = header + out
                        st.session_state.email_history.append({"recipient": recipient, "purpose": purpose, "tone": email_tone, "output": full})
                        st.session_state.total_ops += 1
                        st.success(f"Generated in {round(time.time()-t,1)}s.")
                    except Exception as e:
                        st.error(str(e))

    with col_r:
        st.markdown('<div class="section-header">Generated Email</div>', unsafe_allow_html=True)
        if st.session_state.email_history:
            last = st.session_state.email_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button("Download Email (.txt)", data=last["output"], file_name="email.txt", mime="text/plain", use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:5rem 2rem;color:#aaa;border:1.5px dashed rgba(0,0,0,0.1);border-radius:12px;">
                <div style="font-size:0.9rem;font-weight:600;color:#888;">No email yet</div>
                <div style="font-size:0.8rem;margin-top:0.2rem;">Configure parameters and click Compose.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 — RESUME BUILDER
# ══════════════════════════════════════════════════════════════
with tab_resume:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown('<div class="section-header">Personal Details</div>', unsafe_allow_html=True)
        r_name  = st.text_input("Full Name", placeholder="e.g. Kishanraj B", key="r_name")
        r_title = st.text_input("Target Role", placeholder="e.g. Generative AI Engineer", key="r_title")
        r_email = st.text_input("Email", placeholder="name@email.com", key="r_email")
        r_phone = st.text_input("Phone", placeholder="+91 98765 43210", key="r_phone")
        r_loc   = st.text_input("Location", placeholder="Bengaluru, India", key="r_loc")

        st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Experience & Education</div>', unsafe_allow_html=True)

        r_summary = st.text_area("Summary Notes", placeholder="Brief background and strengths…", height=70, key="r_summary")
        r_exp = st.text_area("Work Experience", placeholder="Company | Role | Dates\n- Achievement with metric\n- Achievement with metric", height=150, key="r_exp")
        r_edu = st.text_area("Education", placeholder="B.E. Computer Science | VTU | 2024 | CGPA: 8.8", height=65, key="r_edu")

        st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Skills & Extras</div>', unsafe_allow_html=True)
        r_skills = st.text_area("Skills", placeholder="Python, Gemini API, FastAPI, Docker, React, Machine Learning, Git", height=65, key="r_skills")

        with st.expander("Projects & Certifications"):
            r_projects = st.text_area("Projects", placeholder="SmartGen AI | AI Career Platform | Python, Streamlit, Gemini", height=80, key="r_proj")
            r_certs = st.text_area("Certifications", placeholder="Google Cloud Professional ML | 2024", height=55, key="r_certs")

        st.markdown(f"""
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:-0.2rem 0 0.8rem;">
            <span class="chip chip-meta">ATS Optimized</span>
            <span class="chip chip-meta">Temp: 0.2</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Resume", use_container_width=True, key="gen_resume"):
            if not api_key: st.error("Enter API key.")
            elif not r_name.strip(): st.warning("Enter full name.")
            elif not r_title.strip(): st.warning("Enter target role.")
            elif not r_exp.strip(): st.warning("Enter work experience.")
            elif not r_skills.strip(): st.warning("Enter skills.")
            else:
                with st.spinner("Building structured ATS resume…"):
                    try:
                        t = time.time()
                        out = generate_resume(
                            r_name, r_title, r_email, r_phone, r_loc,
                            r_summary or "Professional with strong technical background.",
                            r_exp, r_edu or "N/A",
                            r_skills, r_projects or "None", r_certs or "None",
                            api_key, model_choice
                        )
                        fname = f"{r_name.replace(' ','_')}_Resume.txt"
                        st.session_state.resume_history.append({"name": r_name, "title": r_title, "output": out, "file": fname})
                        st.session_state.total_ops += 1
                        st.success(f"Generated in {round(time.time()-t,1)}s.")
                    except Exception as e:
                        st.error(str(e))

    with col_r:
        st.markdown('<div class="section-header">Generated Resume</div>', unsafe_allow_html=True)
        if st.session_state.resume_history:
            last = st.session_state.resume_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(f"Download {last['file']}", data=last["output"], file_name=last["file"], mime="text/plain", use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:5rem 2rem;color:#aaa;border:1.5px dashed rgba(0,0,0,0.1);border-radius:12px;">
                <div style="font-size:0.9rem;font-weight:600;color:#888;">No resume yet</div>
                <div style="font-size:0.8rem;margin-top:0.2rem;">Fill in the form and click Generate.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 5 — HISTORY
# ══════════════════════════════════════════════════════════════
with tab_history:
    has_any = st.session_state.blog_history or st.session_state.email_history or st.session_state.resume_history

    if not has_any:
        st.markdown("""
        <div style="text-align:center;padding:5rem 2rem;color:#aaa;">
            <div style="font-size:0.9rem;font-weight:600;color:#888;">No history yet</div>
            <div style="font-size:0.8rem;margin-top:0.2rem;">Generated content will appear here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.session_state.blog_history or st.session_state.email_history:
            col_b, col_e = st.columns(2, gap="large")

            with col_b:
                st.markdown('<div class="section-header">Articles</div>', unsafe_allow_html=True)
                if st.session_state.blog_history:
                    for i, item in enumerate(reversed(st.session_state.blog_history), 1):
                        with st.expander(f"#{len(st.session_state.blog_history)+1-i} — {item['topic'][:40]}"):
                            st.markdown(f'<div style="display:flex;gap:0.4rem;margin-bottom:0.6rem;"><span class="chip chip-meta">{item["tone"]}</span><span class="chip chip-meta">~{item["words"]} words</span></div>', unsafe_allow_html=True)
                            st.text(item["output"][:800] + ("…" if len(item["output"]) > 800 else ""))
                            st.download_button("Download", data=item["output"], file_name=f"article_{i}.txt", mime="text/plain", key=f"dl_b_{i}")
                else:
                    st.caption("No articles yet.")

            with col_e:
                st.markdown('<div class="section-header">Emails</div>', unsafe_allow_html=True)
                if st.session_state.email_history:
                    for i, item in enumerate(reversed(st.session_state.email_history), 1):
                        with st.expander(f"#{len(st.session_state.email_history)+1-i} — {item['recipient'][:30]}"):
                            st.markdown(f'<div style="display:flex;gap:0.4rem;margin-bottom:0.6rem;"><span class="chip chip-meta">{item["purpose"][:22]}</span><span class="chip chip-meta">{item["tone"]}</span></div>', unsafe_allow_html=True)
                            st.text(item["output"][:600] + ("…" if len(item["output"]) > 600 else ""))
                            st.download_button("Download", data=item["output"], file_name=f"email_{i}.txt", mime="text/plain", key=f"dl_e_{i}")
                else:
                    st.caption("No emails yet.")

        if st.session_state.resume_history:
            st.markdown('<hr style="margin:1rem 0;">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Resumes</div>', unsafe_allow_html=True)
            for i, item in enumerate(reversed(st.session_state.resume_history), 1):
                with st.expander(f"#{len(st.session_state.resume_history)+1-i} — {item['name']} | {item['title'][:30]}"):
                    st.text(item["output"][:800] + ("…" if len(item["output"]) > 800 else ""))
                    st.download_button("Download", data=item["output"], file_name=item["file"], mime="text/plain", key=f"dl_r_{i}")

        st.markdown('<hr style="margin:1.2rem 0;">', unsafe_allow_html=True)
        if st.button("Clear All History", type="secondary", key="clear_history"):
            st.session_state.blog_history = []
            st.session_state.email_history = []
            st.session_state.resume_history = []
            st.session_state.total_ops = 0
            st.rerun()
