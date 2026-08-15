"""
SmartGen AI — Career Intelligence & Content Studio
--------------------------------------------------
Minimalist design: pure white background, black typography, clean glassmorphism.
Powered by Google Gemini REST API.
"""

import streamlit as st
import os
import io
import json
import time
import re

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartGen AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Ultra-Minimalist (White + Black + Glassmorphism)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Global Typography & Tone ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #000000 !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Pure Minimal Light Canvas ── */
.stApp {
    background: #ffffff !important;
    background-image:
        radial-gradient(circle at 10% 15%, rgba(242, 244, 248, 0.8) 0%, transparent 45%),
        radial-gradient(circle at 90% 85%, rgba(244, 242, 248, 0.6) 0%, transparent 45%) !important;
    min-height: 100vh;
}

/* ── Hide Streamlit default chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Universal Black Text ── */
h1, h2, h3, h4, h5, h6, p, span, label, div, strong, em, b {
    color: #000000 !important;
}

/* ── Sidebar — Frosted Glass Panel ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.88) !important;
    backdrop-filter: blur(28px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
    border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.02) !important;
}

[data-testid="stSidebar"] * {
    color: #000000 !important;
}

/* ── Hero Banner — Minimal Editorial Header ── */
.hero-banner {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 20px !important;
    padding: 2.2rem 2.8rem !important;
    margin-bottom: 1.8rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
    position: relative !important;
}

.hero-title {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    color: #000000 !important;
    letter-spacing: -0.04em !important;
    margin: 0 !important;
    line-height: 1.15 !important;
}

.hero-subtitle {
    color: #444444 !important;
    font-size: 0.98rem !important;
    margin-top: 0.4rem !important;
    font-weight: 400 !important;
    letter-spacing: -0.01em !important;
}

/* ── Frosted Glass Cards ── */
.glass-card {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.6rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02) !important;
    margin-bottom: 1rem !important;
}

/* ── Minimalist Glass Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    gap: 6px !important;
}

[data-testid="stTabs"] button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    color: #555555 !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: #000000 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16) !important;
}

[data-testid="stTabs"] button[aria-selected="true"] * {
    color: #ffffff !important;
}

/* ── Input Fields & Controls ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0, 0, 0, 0.14) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #000000 !important;
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06) !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stTextInput label p,
.stNumberInput label p,
.stSlider label p,
.stTextArea label p,
.stRadio label p {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: -0.01em !important;
}

/* ── Buttons — Solid Black with Clean Hover ── */
.stButton > button {
    background: #000000 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1.8rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.14) !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.01em !important;
}

.stButton > button * {
    color: #ffffff !important;
}

.stButton > button:hover {
    background: #222222 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download Buttons ── */
[data-testid="stDownloadButton"] button {
    background: rgba(255, 255, 255, 0.95) !important;
    color: #000000 !important;
    border: 1px solid rgba(0, 0, 0, 0.18) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
}

[data-testid="stDownloadButton"] button * {
    color: #000000 !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: #ffffff !important;
    border-color: #000000 !important;
    transform: translateY(-1px) !important;
}

/* ── Output Box ── */
.output-box {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    border-radius: 14px !important;
    padding: 1.5rem 1.8rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.84rem !important;
    color: #000000 !important;
    line-height: 1.8 !important;
    max-height: 520px !important;
    overflow-y: auto !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.output-box::-webkit-scrollbar { width: 4px; }
.output-box::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.02); border-radius: 2px; }
.output-box::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, 0.18); border-radius: 2px; }

/* ── Section Headers ── */
.section-header {
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    color: #000000 !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
    letter-spacing: -0.02em !important;
}

/* ── Chips / Tags ── */
.metric-row {
    display: flex !important;
    gap: 0.4rem !important;
    flex-wrap: wrap !important;
    margin-bottom: 1rem !important;
}

.metric-chip {
    background: rgba(0, 0, 0, 0.04) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 16px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.78rem !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

.chip-matched {
    background: rgba(0, 0, 0, 0.05) !important;
    border: 1px solid rgba(0, 0, 0, 0.15) !important;
    color: #000000 !important;
    padding: 0.22rem 0.7rem !important;
    border-radius: 16px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    display: inline-block !important;
    margin: 2px !important;
}

.chip-missing {
    background: rgba(220, 38, 38, 0.06) !important;
    border: 1px solid rgba(220, 38, 38, 0.2) !important;
    color: #991b1b !important;
    padding: 0.22rem 0.7rem !important;
    border-radius: 16px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    display: inline-block !important;
    margin: 2px !important;
}

/* ── Score Badge ── */
.score-badge {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #000000 !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    font-size: 1.35rem !important;
    padding: 0.5rem 1.1rem !important;
    border-radius: 12px !important;
}

/* ── Status Indicator ── */
.status-pill {
    background: rgba(0, 0, 0, 0.05) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    color: #000000 !important;
    padding: 0.22rem 0.75rem !important;
    border-radius: 16px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    display: inline-block !important;
}

/* ── Sidebar Stats ── */
.sidebar-stat {
    background: rgba(0, 0, 0, 0.03) !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    border-radius: 10px !important;
    padding: 0.65rem 0.9rem !important;
    margin-bottom: 0.4rem !important;
    color: #000000 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

/* ── Chat Messages ── */
.chat-bubble-user {
    background: #000000 !important;
    color: #ffffff !important;
    padding: 0.9rem 1.2rem !important;
    border-radius: 16px 16px 4px 16px !important;
    margin: 0.5rem 0 0.5rem auto !important;
    max-width: 80% !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
    font-weight: 500 !important;
}

.chat-bubble-user * {
    color: #ffffff !important;
}

.chat-bubble-ai {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    color: #000000 !important;
    padding: 1.1rem 1.4rem !important;
    border-radius: 16px 16px 16px 4px !important;
    margin: 0.5rem auto 0.5rem 0 !important;
    max-width: 88% !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.chat-bubble-ai * {
    color: #000000 !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.75) !important;
    border: 1px dashed rgba(0, 0, 0, 0.18) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 12px !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 12px !important;
    color: #000000 !important;
}

/* ── Divider ── */
hr { border-color: rgba(0, 0, 0, 0.07) !important; }
[data-testid="stHorizontalBlock"] { gap: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper: File Text Extraction (PDF, DOCX, TXT)
# ─────────────────────────────────────────────
def extract_text_from_file(uploaded_file) -> str:
    """Extract plain text from uploaded PDF, DOCX, or TXT file."""
    filename = uploaded_file.name.lower()
    content = ""
    try:
        if filename.endswith(".pdf"):
            import pypdf
            pdf_reader = pypdf.PdfReader(uploaded_file)
            extracted = []
            for page in pdf_reader.pages:
                t = page.extract_text()
                if t:
                    extracted.append(t)
            content = "\n".join(extracted)

        elif filename.endswith(".docx"):
            import docx
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            extracted = [p.text for p in doc.paragraphs if p.text.strip()]
            content = "\n".join(extracted)

        else:
            raw = uploaded_file.read()
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("latin-1", errors="ignore")

    except Exception as e:
        raise ValueError(f"Error reading {filename}: {e}")

    return content.strip()


# ─────────────────────────────────────────────
# Helper: Gemini Direct REST API Call
# ─────────────────────────────────────────────
def call_gemini(system_instruction: str, prompt: str, temperature: float, api_key: str, model: str = "gemini-3.5-flash") -> str:
    """Calls Google Gemini API using direct REST endpoints with multi-model fallback."""
    import requests

    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError("API key is missing. Please enter your Gemini API key in the sidebar.")

    candidate_models = [model, "gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.7-flash"]
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]
    errors = []

    for m in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "systemInstruction": {"parts": [{"text": system_instruction}]},
                "generationConfig": {"temperature": temperature},
            }
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
                errors.append(f"{m}: Empty response")
            else:
                try:
                    err_msg = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    err_msg = resp.text
                errors.append(f"{m} (HTTP {resp.status_code}): {err_msg}")
        except Exception as err:
            errors.append(f"{m}: {err}")

    raise RuntimeError("Generation failed. Details:\n" + "\n".join(errors[-4:]))


# ─────────────────────────────────────────────
# AI Pipeline Functions
# ─────────────────────────────────────────────
def parse_resume_with_ai(resume_text: str, api_key: str, model: str = "gemini-3.5-flash") -> dict:
    """Parse raw resume text into validated, structured profile."""
    system_instruction = (
        "You are an expert Resume Parser and ATS Auditor. "
        "Analyze the resume and return ONLY a valid JSON object matching the exact schema."
    )
    prompt = f"""Extract and structure all information from this resume into the JSON format below.

Resume Text:
\"\"\"{resume_text[:6000]}\"\"\"

Respond ONLY with valid JSON (no markdown):
{{
  "name": "Candidate Full Name",
  "target_role": "Target Role",
  "contact": {{
    "email": "email or N/A",
    "phone": "phone or N/A",
    "location": "location or N/A"
  }},
  "ats_score": 85,
  "summary": "3-sentence professional summary.",
  "skills": {{
    "core_technical": ["Skill 1", "Skill 2"],
    "frameworks_tools": ["Tool 1", "Tool 2"],
    "soft_skills": ["Skill 1", "Skill 2"]
  }},
  "experience": [
    {{
      "role": "Job Title",
      "company": "Company Name",
      "duration": "Dates",
      "highlights": ["Achievement 1", "Achievement 2"]
    }}
  ],
  "education": [
    {{
      "degree": "Degree",
      "institution": "University",
      "year": "Year"
    }}
  ],
  "strengths": ["Strength 1", "Strength 2"],
  "ats_improvements": ["Improvement 1", "Improvement 2"]
}}
"""
    raw_response = call_gemini(system_instruction, prompt, temperature=0.1, api_key=api_key, model=model)
    clean_json = raw_response
    if "```json" in clean_json:
        clean_json = clean_json.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_json:
        clean_json = clean_json.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(clean_json)
    except Exception:
        return {
            "name": "Candidate",
            "target_role": "Software Professional",
            "contact": {"email": "Extracted", "phone": "N/A", "location": "N/A"},
            "ats_score": 80,
            "summary": clean_json[:300],
            "skills": {"core_technical": ["Python", "Engineering"], "frameworks_tools": ["Git", "REST APIs"], "soft_skills": ["Communication"]},
            "experience": [{"role": "Professional Experience", "company": "Company", "duration": "Recent", "highlights": [clean_json[:200]]}],
            "education": [{"degree": "Degree", "institution": "University", "year": "Recent"}],
            "strengths": ["Project Experience"],
            "ats_improvements": ["Quantify achievements with metrics."]
        }


DEFAULT_JOB_CORPUS = [
    {
        "id": "job_1",
        "title": "Generative AI Engineer",
        "company": "AI Labs",
        "domain": "AI / ML",
        "skills_required": ["Python", "Google Gemini API", "LLMs", "RAG", "Prompt Engineering", "Vector DBs", "FastAPI", "Docker"],
        "description": "Build high-throughput RAG systems, integrate multi-modal LLM APIs, and deploy AI applications."
    },
    {
        "id": "job_2",
        "title": "Full Stack Developer",
        "company": "CloudScale",
        "domain": "Web Engineering",
        "skills_required": ["Python", "React", "TypeScript", "FastAPI", "PostgreSQL", "REST APIs", "Docker", "Git"],
        "description": "Design responsive web apps, construct high-performance REST APIs, and manage databases."
    },
    {
        "id": "job_3",
        "title": "Data Scientist",
        "company": "Apex Analytics",
        "domain": "Data Science",
        "skills_required": ["Python", "SQL", "Pandas", "Scikit-Learn", "TensorFlow", "Statistics", "Machine Learning"],
        "description": "Analyze large datasets, develop predictive models, and deploy machine learning pipelines."
    },
    {
        "id": "job_4",
        "title": "Cloud DevOps Architect",
        "company": "Nebula Cloud",
        "domain": "Infrastructure",
        "skills_required": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux", "Python", "Security"],
        "description": "Maintain cloud infrastructure, automate deployment pipelines, and implement observability."
    },
    {
        "id": "job_5",
        "title": "Frontend Engineer",
        "company": "Interface Labs",
        "domain": "Frontend",
        "skills_required": ["React", "Next.js", "JavaScript", "TypeScript", "CSS", "REST APIs", "UI/UX", "Git"],
        "description": "Craft high-performance web user interfaces with clean architecture and responsive design."
    }
]


def match_resume_to_jobs(parsed_profile: dict, job_list: list, api_key: str, model: str = "gemini-3.5-flash") -> list:
    """Match candidate profile against job corpus and compute match scores."""
    profile_summary = f"Candidate Target Role: {parsed_profile.get('target_role', '')}\nSkills: {json.dumps(parsed_profile.get('skills', {}))}\nSummary: {parsed_profile.get('summary', '')}"
    jobs_summary = json.dumps([{"id": j["id"], "title": j["title"], "company": j["company"], "skills_required": j["skills_required"]} for j in job_list])

    system_instruction = "Calculate semantic match score (0-100%) between candidate profile and each job. Return ONLY valid JSON array."
    prompt = f"Candidate Profile:\n{profile_summary}\n\nJobs List:\n{jobs_summary}\n\nRespond ONLY with JSON array:\n[{{\"id\": \"job_id\", \"match_score\": 85, \"matched_skills\": [\"Skill 1\"], \"missing_skills\": [\"Skill 2\"], \"fit_summary\": \"Assessment.\"}}]"

    raw = call_gemini(system_instruction, prompt, temperature=0.1, api_key=api_key, model=model)
    clean_json = raw
    if "```json" in clean_json:
        clean_json = clean_json.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_json:
        clean_json = clean_json.split("```")[1].split("```")[0].strip()

    try:
        scores = json.loads(clean_json)
        score_dict = {s["id"]: s for s in scores}
    except Exception:
        score_dict = {}

    results = []
    for job in job_list:
        jid = job["id"]
        if jid in score_dict:
            res = {**job, **score_dict[jid]}
        else:
            cand_skills = set(
                [s.lower() for s in parsed_profile.get("skills", {}).get("core_technical", [])] +
                [s.lower() for s in parsed_profile.get("skills", {}).get("frameworks_tools", [])]
            )
            job_skills = job.get("skills_required", [])
            matched = [s for s in job_skills if s.lower() in cand_skills]
            missing = [s for s in job_skills if s.lower() not in cand_skills]
            score = int((len(matched) / max(len(job_skills), 1)) * 100)
            res = {
                **job,
                "match_score": score,
                "matched_skills": matched,
                "missing_skills": missing,
                "fit_summary": f"Matches {len(matched)} of {len(job_skills)} key requirements."
            }
        results.append(res)

    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return results


def generate_cv_suggestions(parsed_profile: dict, target_job: dict, api_key: str, model: str = "gemini-3.5-flash") -> str:
    """Generate tailored CV suggestions and optimized content."""
    system_instruction = "You are an Executive Resume Strategist. Provide actionable, high-impact CV optimization tailored to the target job."
    prompt = f"""Candidate Profile:\n{json.dumps(parsed_profile, indent=2)}\n\nTarget Job:\nRole: {target_job.get('title')} at {target_job.get('company')}\nRequired: {', '.join(target_job.get('skills_required', []))}\nDescription: {target_job.get('description', '')}

Provide structured recommendations using '━━━' dividers:

1. TARGETED PROFESSIONAL SUMMARY
Polished 3-4 sentence summary tailored for {target_job.get('title')}.

2. MISSING KEYWORDS & SKILLS
High-value technical keywords required for this position.

3. BULLET POINT REWRITES (XYZ FORMULA)
3 rewritten experience bullets: 'Accomplished [X] measured by [Y] by doing [Z]'.

4. ATS READABILITY AUDIT
3 specific points to pass enterprise ATS filters.

5. TAILORED RESUME DRAFT
Clean text resume preview.
"""
    return call_gemini(system_instruction, prompt, temperature=0.3, api_key=api_key, model=model)


def career_mentor_chat(messages: list, candidate_context: str, job_context: str, api_key: str, model: str = "gemini-3.5-flash") -> str:
    """Grounded career advisor chatbot."""
    system_instruction = f"""You are SmartGen Career Mentor — a professional career advisor and talent coach.
Candidate Context: {candidate_context}
Target Job Context: {job_context}

Provide direct, actionable career coaching, mock interview frameworks, and learning roadmaps. Keep a clean, professional tone without emojis.
"""
    chat_history_str = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Advisor"
        chat_history_str += f"{role}: {msg['content']}\n\n"

    prompt = f"Transcript:\n{chat_history_str}\n\nRespond constructively to the user's latest query."
    return call_gemini(system_instruction, prompt, temperature=0.5, api_key=api_key, model=model)


def generate_blog(topic: str, tone: str, word_count: int, api_key: str, model: str = "gemini-3.5-flash") -> str:
    system_instruction = "You are an experienced article writer who crafts clear, insightful, well-structured articles."
    prompt = f"""Write an article based on:
- Topic: "{topic}"
- Tone: {tone}
- Target Word Count: {word_count} words

Structure:
1. Title: Clean, engaging title.
2. Introduction: Strong opening hook.
3. Body Sections: 2-3 focused sections with subheadings.
4. Conclusion: Clear takeaway or summary.
"""
    return call_gemini(system_instruction, prompt, temperature=0.7, api_key=api_key, model=model)


def generate_email(recipient: str, purpose: str, tone: str, api_key: str, model: str = "gemini-3.5-flash") -> str:
    system_instruction = "You are a professional communication specialist who drafts polished, concise emails."
    prompt = f"""Write a professional email:
- Recipient: {recipient}
- Purpose: {purpose}
- Tone: {tone}

Structure:
1. Subject Line: Concise, direct subject.
2. Salutation: Appropriate greeting.
3. Body: Clear message addressing {purpose}.
4. Sign-off: Professional closing with sender placeholders.
"""
    return call_gemini(system_instruction, prompt, temperature=0.3, api_key=api_key, model=model)


def generate_resume(
    name: str, job_title: str, email: str, phone: str, location: str,
    summary: str, experience: str, education: str, skills: str,
    projects: str, certifications: str, api_key: str, model: str = "gemini-3.5-flash"
) -> str:
    system_instruction = "You are a professional resume writer crafting ATS-optimized resumes with strong action verbs and quantified achievements."
    prompt = f"""Build an ATS-friendly resume from these details:

Candidate:
- Name: {name}
- Target Role: {job_title}
- Email: {email}
- Phone: {phone}
- Location: {location}

Summary: {summary}
Experience: {experience}
Education: {education}
Skills: {skills}
Projects: {projects}
Certifications: {certifications}

Formatting:
1. Header: Name & contact details.
2. Summary: 3-4 sentence professional summary.
3. Experience: Reverse-chronological bullet points with action verbs.
4. Education: Degree, institution, year.
5. Skills: Categorized.
6. Projects & Certifications: If provided.
Use ━━━ section dividers.
"""
    return call_gemini(system_instruction, prompt, temperature=0.2, api_key=api_key, model=model)


# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────
if "blog_history" not in st.session_state:
    st.session_state.blog_history = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []
if "resume_history" not in st.session_state:
    st.session_state.resume_history = []
if "parsed_profile" not in st.session_state:
    st.session_state.parsed_profile = None
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "cv_suggestions_output" not in st.session_state:
    st.session_state.cv_suggestions_output = None
if "mentor_messages" not in st.session_state:
    st.session_state.mentor_messages = [
        {"role": "assistant", "content": "Hello. I am your Career Advisor. Upload a resume or select a target job to begin interview preparation, skill roadmapping, or cover letter generation."}
    ]
if "total_generated" not in st.session_state:
    st.session_state.total_generated = 0


# ─────────────────────────────────────────────
# Sidebar — Minimalist Configuration
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 0 1.2rem;">
        <div style="font-size:1.25rem; font-weight:900; color:#000000; letter-spacing:-0.03em;">SmartGen AI</div>
        <div style="color:#666666; font-size:0.8rem; margin-top:0.2rem; font-weight:500;">
            Career Intelligence & Content Studio
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**API Configuration**")
    default_key = ""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            default_key = st.secrets["GEMINI_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets:
            default_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass
    if not default_key:
        default_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=default_key,
        placeholder="Enter API key",
        help="Google Gemini API Key",
    )

    model_choice = st.selectbox(
        "Model",
        options=["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.7-flash"],
        index=0,
    )

    if api_key:
        st.markdown('<div class="status-pill">Key Ready</div>', unsafe_allow_html=True)
    else:
        st.caption("Enter API key to enable generation.")

    st.divider()

    st.markdown("**Session Overview**")
    has_profile = "Active" if st.session_state.parsed_profile else "None"
    matched_title = st.session_state.selected_job['title'] if st.session_state.selected_job else "None"
    st.markdown(f"""
    <div class="sidebar-stat">Profile: <strong>{has_profile}</strong></div>
    <div class="sidebar-stat">Target: <strong>{matched_title[:20]}</strong></div>
    <div class="sidebar-stat">Articles: <strong>{len(st.session_state.blog_history)}</strong></div>
    <div class="sidebar-stat">Emails: <strong>{len(st.session_state.email_history)}</strong></div>
    <div class="sidebar-stat">Resumes: <strong>{len(st.session_state.resume_history)}</strong></div>
    <div class="sidebar-stat">Operations: <strong>{st.session_state.total_generated}</strong></div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Minimal Editorial Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">SmartGen AI</div>
    <div class="hero-subtitle">Intelligent Career Intelligence &amp; Content Platform.</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Main Navigation Tabs
# ─────────────────────────────────────────────
tab_career, tab_blog, tab_email, tab_resume_builder, tab_history = st.tabs([
    "Career Intelligence",
    "Blog Studio",
    "Email Writer",
    "Resume Builder",
    "History",
])


# ══════════════════════════════════════════════
# TAB 1 — CAREER INTELLIGENCE
# ══════════════════════════════════════════════
with tab_career:
    career_step = st.radio(
        "Pipeline Step:",
        options=[
            "1. Resume Parser",
            "2. Job Matching",
            "3. CV Optimization",
            "4. Career Mentor",
        ],
        horizontal=True,
        key="career_pipeline_step"
    )

    st.markdown("---")

    # ──────────────────────────────────────────
    # STEP 1: RESUME PARSER
    # ──────────────────────────────────────────
    if "1. Resume Parser" in career_step:
        col_upload, col_profile = st.columns([1, 1], gap="large")

        with col_upload:
            st.markdown('<div class="section-header">Resume Document</div>', unsafe_allow_html=True)

            upload_mode = st.radio("Input Method:", ["Upload File (PDF, DOCX, TXT)", "Paste Plain Text"], horizontal=True)

            resume_content = ""
            if upload_mode == "Upload File (PDF, DOCX, TXT)":
                uploaded_file = st.file_uploader(
                    "Select Resume File",
                    type=["pdf", "docx", "txt"],
                )
                if uploaded_file:
                    try:
                        resume_content = extract_text_from_file(uploaded_file)
                        st.caption(f"Extracted {len(resume_content.split())} words from {uploaded_file.name}")
                        with st.expander("View Extracted Text"):
                            st.text(resume_content[:1200] + ("..." if len(resume_content) > 1200 else ""))
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                resume_content = st.text_area(
                    "Resume Text",
                    placeholder="Paste resume text including contact, skills, experience, and education...",
                    height=280
                )

            parse_btn = st.button("Analyze Resume", use_container_width=True, key="parse_resume_btn")

            if parse_btn:
                if not api_key:
                    st.error("Enter Gemini API key in sidebar.")
                elif not resume_content.strip():
                    st.warning("Upload a file or paste resume content.")
                else:
                    with st.spinner("Analyzing resume and computing ATS readiness…"):
                        try:
                            start = time.time()
                            parsed = parse_resume_with_ai(resume_content, api_key=api_key, model=model_choice)
                            elapsed = round(time.time() - start, 1)

                            st.session_state.parsed_profile = parsed
                            st.session_state.raw_resume_text = resume_content
                            st.session_state.total_generated += 1
                            st.success(f"Resume parsed in {elapsed}s.")
                        except Exception as e:
                            st.error(f"Error: {e}")

        with col_profile:
            st.markdown('<div class="section-header">Candidate Profile</div>', unsafe_allow_html=True)

            profile = st.session_state.parsed_profile
            if profile:
                ats_score = profile.get("ats_score", 80)
                col_score, col_meta = st.columns([1, 2])
                with col_score:
                    st.markdown(f"""
                    <div style="text-align:center; padding:1.2rem; background:rgba(0,0,0,0.03); border-radius:12px; border:1px solid rgba(0,0,0,0.08);">
                        <div style="font-size:0.75rem; color:#666666; font-weight:700; text-transform:uppercase;">ATS Readiness</div>
                        <div class="score-badge" style="margin-top:0.4rem;">{ats_score}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_meta:
                    st.markdown(f"""
                    <div style="padding:0.3rem 0;">
                        <div style="font-size:1.3rem; font-weight:900; color:#000000;">{profile.get('name', 'Candidate')}</div>
                        <div style="font-size:0.92rem; font-weight:700; color:#333333;">{profile.get('target_role', 'Target Role')}</div>
                        <div style="font-size:0.8rem; color:#666666; margin-top:0.25rem;">
                            Location: {profile.get('contact', {}).get('location', 'N/A')} | Email: {profile.get('contact', {}).get('email', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("**Executive Summary**")
                st.markdown(f"""<div style="font-size:0.88rem; color:#222222; line-height:1.6; background:rgba(255,255,255,0.7); padding:0.8rem; border-radius:10px; border:1px solid rgba(0,0,0,0.06);">{profile.get('summary', 'No summary available.')}</div>""", unsafe_allow_html=True)

                st.markdown("**Extracted Skills**")
                skills_data = profile.get("skills", {})
                if isinstance(skills_data, dict):
                    for cat, s_list in skills_data.items():
                        cat_title = cat.replace("_", " ").title()
                        st.markdown(f"<span style='font-size:0.78rem; font-weight:700; color:#444444;'>{cat_title}:</span>", unsafe_allow_html=True)
                        chips_html = "".join([f"<span class='metric-chip' style='margin:2px;'>{s}</span>" for s in s_list])
                        st.markdown(f"<div style='margin-bottom:0.5rem;'>{chips_html}</div>", unsafe_allow_html=True)

                st.markdown("**Work Experience**")
                for exp in profile.get("experience", []):
                    with st.expander(f"{exp.get('role', 'Role')} — {exp.get('company', 'Company')} ({exp.get('duration', 'Dates')})"):
                        for hl in exp.get("highlights", []):
                            st.markdown(f"- {hl}")

                if profile.get("ats_improvements"):
                    st.markdown("**ATS Recommendations**")
                    for tip in profile.get("ats_improvements", []):
                        st.markdown(f"- {tip}")
            else:
                st.markdown("""
                <div style="text-align:center; padding:4rem 2rem; color:#777777;">
                    <div style="font-size:0.95rem; font-weight:600;">No Profile Loaded</div>
                    <div style="font-size:0.82rem; margin-top:0.3rem;">Upload a resume on the left to extract structured candidate data.</div>
                </div>
                """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # STEP 2: JOB MATCHING
    # ──────────────────────────────────────────
    elif "2. Job Matching" in career_step:
        st.markdown('<div class="section-header">Job Matching & Gap Analysis</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("Parse a resume in Step 1 to match positions.")
        else:
            col_cfg, col_jobs = st.columns([1, 2], gap="large")

            with col_cfg:
                st.markdown("**Job Source**")
                job_source = st.radio(
                    "Select Source:",
                    ["Built-in Target Corpus", "Custom Job Posting"],
                    key="job_source_mode"
                )

                active_jobs = list(DEFAULT_JOB_CORPUS)
                if job_source == "Custom Job Posting":
                    c_title = st.text_input("Title", value="Generative AI Engineer")
                    c_company = st.text_input("Organization", value="Enterprise AI")
                    c_skills = st.text_input("Key Requirements", value="Python, Gemini API, RAG, Streamlit, Docker")
                    c_desc = st.text_area("Job Description", height=140, value="Building LLM-powered applications and vector search.")

                    custom_job = {
                        "id": "custom_job_1",
                        "title": c_title,
                        "company": c_company,
                        "domain": "Target Role",
                        "skills_required": [s.strip() for s in c_skills.split(",") if s.strip()],
                        "description": c_desc
                    }
                    active_jobs = [custom_job] + DEFAULT_JOB_CORPUS

                match_btn = st.button("Match Positions", use_container_width=True, key="run_match_btn")

            with col_jobs:
                st.markdown("**Ranked Positions**")

                if match_btn or "matched_jobs_list" in st.session_state:
                    if match_btn:
                        if not api_key:
                            st.error("Enter Gemini API key.")
                        else:
                            with st.spinner("Calculating semantic alignment…"):
                                try:
                                    st.session_state.matched_jobs_list = match_resume_to_jobs(
                                        st.session_state.parsed_profile,
                                        active_jobs,
                                        api_key=api_key,
                                        model=model_choice
                                    )
                                    st.session_state.total_generated += 1
                                except Exception as e:
                                    st.error(f"Error: {e}")

                    matched_jobs = st.session_state.get("matched_jobs_list", [])
                    if matched_jobs:
                        for idx, job in enumerate(matched_jobs):
                            score = job.get("match_score", 70)
                            with st.container():
                                st.markdown(f"""
                                <div class="glass-card" style="padding:1.3rem; margin-bottom:0.8rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <div>
                                            <div style="font-size:1.1rem; font-weight:800; color:#000000;">{job['title']}</div>
                                            <div style="font-size:0.85rem; color:#555555; font-weight:600;">{job['company']} — {job.get('domain', 'Industry')}</div>
                                        </div>
                                        <div>
                                            <span style="background:#000000; color:#ffffff; font-weight:800; font-size:1rem; padding:0.35rem 0.8rem; border-radius:10px;">
                                                {score}% Match
                                            </span>
                                        </div>
                                    </div>
                                    <div style="margin-top:0.6rem; font-size:0.84rem; color:#333333;">
                                        {job.get('fit_summary', job.get('description', '')[:140])}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                col_m, col_g, col_act = st.columns([1, 1, 0.8])
                                with col_m:
                                    st.markdown("<span style='font-size:0.75rem; font-weight:700;'>Matched:</span>", unsafe_allow_html=True)
                                    matched_chips = "".join([f"<span class='chip-matched'>{s}</span>" for s in job.get("matched_skills", [])]) or "<span style='font-size:0.75rem; color:#777;'>None</span>"
                                    st.markdown(matched_chips, unsafe_allow_html=True)
                                with col_g:
                                    st.markdown("<span style='font-size:0.75rem; font-weight:700; color:#991b1b;'>Missing:</span>", unsafe_allow_html=True)
                                    missing_chips = "".join([f"<span class='chip-missing'>{s}</span>" for s in job.get("missing_skills", [])]) or "<span style='font-size:0.75rem;'>None</span>"
                                    st.markdown(missing_chips, unsafe_allow_html=True)
                                with col_act:
                                    if st.button(f"Target Position", key=f"select_job_{job['id']}_{idx}"):
                                        st.session_state.selected_job = job
                                        st.success(f"Selected: {job['title']}")
                                st.markdown("---")
                    else:
                        st.caption("Click Match Positions to evaluate fit.")

    # ──────────────────────────────────────────
    # STEP 3: CV OPTIMIZATION
    # ──────────────────────────────────────────
    elif "3. CV Optimization" in career_step:
        st.markdown('<div class="section-header">CV Optimization & Bullet Rewriter</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("Parse a resume in Step 1 to optimize.")
        else:
            col_target, col_out = st.columns([1, 1.4], gap="large")

            with col_target:
                st.markdown("**Target Position**")
                job_options = [j["title"] + f" ({j['company']})" for j in DEFAULT_JOB_CORPUS]
                sel_idx = 0
                if st.session_state.selected_job:
                    cur_title = st.session_state.selected_job["title"]
                    for i, opt in enumerate(job_options):
                        if cur_title in opt:
                            sel_idx = i
                            break

                chosen_opt = st.selectbox("Position", job_options, index=sel_idx)
                selected_job_obj = DEFAULT_JOB_CORPUS[0]
                for j in DEFAULT_JOB_CORPUS:
                    if j["title"] in chosen_opt:
                        selected_job_obj = j
                        break

                if st.session_state.selected_job:
                    selected_job_obj = st.session_state.selected_job

                st.markdown(f"""
                <div class="glass-card" style="padding:1.1rem; margin-top:0.5rem;">
                    <div style="font-weight:800; font-size:1rem;">{selected_job_obj['title']}</div>
                    <div style="color:#555555; font-size:0.82rem;">{selected_job_obj['company']}</div>
                    <div style="margin-top:0.5rem; font-size:0.78rem; color:#333333;">
                        <strong>Requirements:</strong> {', '.join(selected_job_obj.get('skills_required', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                generate_sugg_btn = st.button("Optimize CV", use_container_width=True, key="gen_cv_sugg_btn")

            with col_out:
                st.markdown('<div class="section-header">Optimization Plan</div>', unsafe_allow_html=True)

                if generate_sugg_btn:
                    if not api_key:
                        st.error("Enter Gemini API key.")
                    else:
                        with st.spinner("Synthesizing tailored recommendations and XYZ bullet rewrites…"):
                            try:
                                start = time.time()
                                suggestions = generate_cv_suggestions(
                                    st.session_state.parsed_profile,
                                    selected_job_obj,
                                    api_key=api_key,
                                    model=model_choice
                                )
                                elapsed = round(time.time() - start, 1)

                                st.session_state.cv_suggestions_output = suggestions
                                st.session_state.total_generated += 1
                                st.success(f"Generated in {elapsed}s.")
                            except Exception as e:
                                st.error(f"Error: {e}")

                if st.session_state.cv_suggestions_output:
                    output_text = st.session_state.cv_suggestions_output
                    st.markdown(f'<div class="output-box">{output_text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "Download Optimization Plan",
                        data=output_text,
                        file_name=f"Tailored_{selected_job_obj['title'].replace(' ', '_')}_CV.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                else:
                    st.markdown("""
                    <div style="text-align:center; padding:3.5rem 2rem; color:#777777;">
                        <div style="font-size:0.9rem; font-weight:600;">Optimization Ready</div>
                        <div style="font-size:0.8rem; margin-top:0.25rem;">Select target position and click Optimize CV.</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # STEP 4: CAREER MENTOR
    # ──────────────────────────────────────────
    elif "4. Career Mentor" in career_step:
        st.markdown('<div class="section-header">Career Mentor</div>', unsafe_allow_html=True)

        col_chat_cfg, col_chat_main = st.columns([1, 2.2], gap="large")

        with col_chat_cfg:
            st.markdown("**Grounded Context**")
            profile_ctx = "No profile uploaded"
            if st.session_state.parsed_profile:
                p = st.session_state.parsed_profile
                profile_ctx = f"Candidate: {p.get('name')} | Role: {p.get('target_role')} | Skills: {p.get('skills')}"

            job_ctx = "General Tech Industry"
            if st.session_state.selected_job:
                j = st.session_state.selected_job
                job_ctx = f"Position: {j.get('title')} at {j.get('company')} | Requirements: {j.get('skills_required')}"

            st.markdown(f"""
            <div class="sidebar-stat" style="font-size:0.78rem; line-height:1.5;">
                <strong>Candidate:</strong><br>{profile_ctx[:110]}...<br><br>
                <strong>Target:</strong><br>{job_ctx[:110]}...
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Quick Prompts**")
            q1 = st.button("Mock Interview Questions", use_container_width=True)
            q2 = st.button("60-Day Learning Plan", use_container_width=True)
            q3 = st.button("Draft Cover Letter", use_container_width=True)
            q4 = st.button("Salary Strategy", use_container_width=True)

            auto_prompt = None
            if q1:
                auto_prompt = "Generate 5 interview questions tailored to my resume and target role with STAR method answer frameworks."
            elif q2:
                auto_prompt = "Create a structured 60-day step-by-step milestone learning plan to bridge missing skills."
            elif q3:
                auto_prompt = "Write a concise cover letter tailored to this position highlighting relevant accomplishments."
            elif q4:
                auto_prompt = "Provide a salary negotiation script and benchmark strategy for this role."

            if st.button("Reset Conversation", use_container_width=True):
                st.session_state.mentor_messages = [
                    {"role": "assistant", "content": "Conversation reset. How can I assist your career progression?"}
                ]
                st.rerun()

        with col_chat_main:
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.mentor_messages:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

            user_input = st.chat_input("Ask a question regarding interview prep, roadmaps, or applications...")
            final_input = auto_prompt or user_input

            if final_input:
                if not api_key:
                    st.error("Enter Gemini API key.")
                else:
                    st.session_state.mentor_messages.append({"role": "user", "content": final_input})
                    st.markdown(f'<div class="chat-bubble-user">{final_input}</div>', unsafe_allow_html=True)

                    with st.spinner("Thinking…"):
                        try:
                            start = time.time()
                            ai_reply = career_mentor_chat(
                                st.session_state.mentor_messages,
                                candidate_context=profile_ctx,
                                job_context=job_ctx,
                                api_key=api_key,
                                model=model_choice
                            )
                            st.session_state.mentor_messages.append({"role": "assistant", "content": ai_reply})
                            st.session_state.total_generated += 1
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")


# ══════════════════════════════════════════════
# TAB 2 — BLOG STUDIO
# ══════════════════════════════════════════════
with tab_blog:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">Article Parameters</div>', unsafe_allow_html=True)

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Modern Software Architecture Patterns",
            value="Modern Software Architecture Patterns",
        )

        tone = st.selectbox(
            "Tone",
            options=["professional", "formal", "casual", "analytical", "executive"],
            index=0,
        )

        word_count = st.slider(
            "Target Word Count",
            min_value=100,
            max_value=1500,
            value=350,
            step=50,
        )

        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-chip">Temperature: 0.7</span>
            <span class="metric-chip">Length: ~{word_count} words</span>
            <span class="metric-chip">Tone: {tone}</span>
        </div>
        """, unsafe_allow_html=True)

        generate_blog_btn = st.button("Generate Article", use_container_width=True, key="gen_blog")

    with col_right:
        st.markdown('<div class="section-header">Generated Article</div>', unsafe_allow_html=True)

        if generate_blog_btn:
            if not api_key:
                st.error("Enter Gemini API key.")
            elif not topic.strip():
                st.warning("Enter a topic.")
            else:
                with st.spinner("Generating article…"):
                    try:
                        start = time.time()
                        blog_text = generate_blog(topic, tone, word_count, api_key, model=model_choice)
                        elapsed = round(time.time() - start, 1)

                        header = f"ARTICLE GENERATOR\nTopic: \"{topic}\"\nTone: {tone}\nTarget Length: {word_count} words\n\n"
                        full_output = header + blog_text

                        st.session_state.blog_history.append({
                            "topic": topic,
                            "tone": tone,
                            "word_count": word_count,
                            "output": full_output,
                        })
                        st.session_state.total_generated += 1

                        st.success(f"Generated in {elapsed}s.")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "Download Article (.txt)",
                            data=full_output,
                            file_name="article_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif st.session_state.blog_history:
            last = st.session_state.blog_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "Download Article (.txt)",
                data=last["output"],
                file_name="article_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:#777777;">
                <div style="font-size:0.9rem; font-weight:600;">No Article Generated</div>
                <div style="font-size:0.8rem; margin-top:0.25rem;">Configure parameters and click Generate Article.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — EMAIL WRITER
# ══════════════════════════════════════════════
with tab_email:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">Email Parameters</div>', unsafe_allow_html=True)

        recipient = st.text_input(
            "Recipient",
            placeholder="e.g. Hiring Manager",
            value="Hiring Manager",
        )

        purpose = st.selectbox(
            "Purpose",
            options=[
                "Interview Follow-up",
                "Cold Outreach",
                "Status Update",
                "Meeting Request",
                "Offer Inquiry",
                "Custom",
            ],
            index=0,
        )

        if purpose == "Custom":
            purpose = st.text_input("Specify Purpose:", placeholder="Describe email objective")

        email_tone = st.selectbox(
            "Tone",
            options=["professional", "formal", "direct", "concise"],
            index=0,
        )

        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-chip">Temperature: 0.3</span>
            <span class="metric-chip">Tone: {email_tone}</span>
        </div>
        """, unsafe_allow_html=True)

        generate_email_btn = st.button("Compose Email", use_container_width=True, key="gen_email")

    with col_right:
        st.markdown('<div class="section-header">Generated Email</div>', unsafe_allow_html=True)

        if generate_email_btn:
            if not api_key:
                st.error("Enter Gemini API key.")
            elif not recipient.strip():
                st.warning("Enter recipient.")
            elif not purpose or not purpose.strip():
                st.warning("Enter purpose.")
            else:
                with st.spinner("Composing email…"):
                    try:
                        start = time.time()
                        email_text = generate_email(recipient, purpose, email_tone, api_key, model=model_choice)
                        elapsed = round(time.time() - start, 1)

                        header = f"EMAIL COMPOSER\nRecipient: {recipient}\nPurpose: {purpose}\nTone: {email_tone}\n\n"
                        full_output = header + email_text

                        st.session_state.email_history.append({
                            "recipient": recipient,
                            "purpose": purpose,
                            "tone": email_tone,
                            "output": full_output,
                        })
                        st.session_state.total_generated += 1

                        st.success(f"Generated in {elapsed}s.")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "Download Email (.txt)",
                            data=full_output,
                            file_name="email_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif st.session_state.email_history:
            last = st.session_state.email_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "Download Email (.txt)",
                data=last["output"],
                file_name="email_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:#777777;">
                <div style="font-size:0.9rem; font-weight:600;">No Email Generated</div>
                <div style="font-size:0.8rem; margin-top:0.25rem;">Configure parameters and click Compose Email.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — RESUME BUILDER
# ══════════════════════════════════════════════
with tab_resume_builder:
    st.markdown('<div class="section-header">Resume Parameters</div>', unsafe_allow_html=True)

    col_form, col_out = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("**Personal Details**")
        r_name     = st.text_input("Full Name",          placeholder="e.g. Kishanraj B", key="rb_name")
        r_title    = st.text_input("Target Role",        placeholder="e.g. AI Engineer", key="rb_title")
        r_email    = st.text_input("Email",              placeholder="name@email.com", key="rb_email")
        r_phone    = st.text_input("Phone",              placeholder="+91 98765 43210", key="rb_phone")
        r_location = st.text_input("Location",           placeholder="Bengaluru, India", key="rb_location")

        st.markdown("---")
        st.markdown("**Executive Summary Notes**")
        r_summary = st.text_area(
            "Summary Notes",
            placeholder="Brief overview of background and core strengths...",
            height=80, key="rb_summary"
        )

        st.markdown("---")
        st.markdown("**Work Experience**")
        r_experience = st.text_area(
            "Role History",
            placeholder="Company | Title | Dates\n- Achievement 1\n- Achievement 2",
            height=150, key="rb_experience"
        )

        st.markdown("---")
        st.markdown("**Education**")
        r_education = st.text_area(
            "Degrees",
            placeholder="Degree | Institution | Year",
            height=65, key="rb_education"
        )

        st.markdown("---")
        st.markdown("**Skills**")
        r_skills = st.text_area(
            "Skills",
            placeholder="Python, Gemini API, Docker, FastAPI, Git, Architecture",
            height=65, key="rb_skills"
        )

        st.markdown("---")
        with st.expander("Projects & Certifications"):
            r_projects = st.text_area("Projects", placeholder="Project Name | Description | Stack", height=80, key="rb_projects")
            r_certifications = st.text_area("Certifications", placeholder="Certificate | Issuer | Year", height=60, key="rb_certs")

        st.markdown(f"""
        <div class="metric-row" style="margin-top:0.4rem;">
            <span class="metric-chip">Temperature: 0.2</span>
            <span class="metric-chip">Format: ATS Structured</span>
        </div>
        """, unsafe_allow_html=True)

        build_resume_btn = st.button("Generate Resume", use_container_width=True, key="rb_build_btn")

    with col_out:
        st.markdown('<div class="section-header">Generated Resume</div>', unsafe_allow_html=True)

        if build_resume_btn:
            if not api_key:
                st.error("Enter Gemini API key.")
            elif not r_name.strip():
                st.warning("Enter name.")
            elif not r_title.strip():
                st.warning("Enter target role.")
            elif not r_experience.strip():
                st.warning("Enter work experience.")
            elif not r_skills.strip():
                st.warning("Enter skills.")
            else:
                with st.spinner("Building structured resume…"):
                    try:
                        start = time.time()
                        resume_text = generate_resume(
                            name=r_name, job_title=r_title,
                            email=r_email, phone=r_phone, location=r_location,
                            summary=r_summary or "Professional with proven background.",
                            experience=r_experience, education=r_education or "N/A",
                            skills=r_skills, projects=r_projects or "None",
                            certifications=r_certifications or "None",
                            api_key=api_key, model=model_choice
                        )
                        elapsed = round(time.time() - start, 1)

                        file_name = f"{r_name.replace(' ', '_')}_Resume.txt"
                        st.session_state.resume_history.append({
                            "name": r_name,
                            "title": r_title,
                            "output": resume_text,
                            "file": file_name,
                        })
                        st.session_state.total_generated += 1

                        st.success(f"Generated in {elapsed}s.")
                        st.markdown(f'<div class="output-box">{resume_text}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "Download Resume (.txt)",
                            data=resume_text,
                            file_name=file_name,
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif st.session_state.resume_history:
            last = st.session_state.resume_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "Download Resume (.txt)",
                data=last["output"],
                file_name=last["file"],
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:#777777;">
                <div style="font-size:0.9rem; font-weight:600;">No Resume Generated</div>
                <div style="font-size:0.8rem; margin-top:0.25rem;">Complete details and click Generate Resume.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — HISTORY
# ══════════════════════════════════════════════
with tab_history:
    col_b, col_e = st.columns(2, gap="large")

    with col_b:
        st.markdown('<div class="section-header">Article Archive</div>', unsafe_allow_html=True)
        if st.session_state.blog_history:
            for i, item in enumerate(reversed(st.session_state.blog_history), 1):
                with st.expander(f"#{len(st.session_state.blog_history)+1-i} — {item['topic'][:45]}"):
                    st.text(item["output"])
                    st.download_button("Download", data=item["output"],
                                       file_name=f"article_{i}.txt", mime="text/plain",
                                       key=f"dl_blog_{i}")
        else:
            st.caption("No articles generated yet.")

    with col_e:
        st.markdown('<div class="section-header">Email Archive</div>', unsafe_allow_html=True)
        if st.session_state.email_history:
            for i, item in enumerate(reversed(st.session_state.email_history), 1):
                with st.expander(f"#{len(st.session_state.email_history)+1-i} — {item['recipient'][:35]}"):
                    st.text(item["output"])
                    st.download_button("Download", data=item["output"],
                                       file_name=f"email_{i}.txt", mime="text/plain",
                                       key=f"dl_email_{i}")
        else:
            st.caption("No emails generated yet.")

    if st.session_state.resume_history:
        st.divider()
        st.markdown('<div class="section-header">Resume Archive</div>', unsafe_allow_html=True)
        for i, item in enumerate(reversed(st.session_state.resume_history), 1):
            with st.expander(f"#{len(st.session_state.resume_history)+1-i} — {item['name']} | {item['title'][:35]}"):
                st.text(item["output"])
                st.download_button("Download", data=item["output"],
                                   file_name=item["file"], mime="text/plain",
                                   key=f"dl_resume_{i}")

    if st.session_state.blog_history or st.session_state.email_history or st.session_state.resume_history:
        st.divider()
        if st.button("Clear Archive", type="secondary"):
            st.session_state.blog_history  = []
            st.session_state.email_history = []
            st.session_state.resume_history = []
            st.session_state.total_generated = 0
            st.rerun()
