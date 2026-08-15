"""
SmartGen AI — AI Career & Content Intelligence Studio
------------------------------------------------------
Minimalistic glassmorphism UI — white background, black text, frosted glass cards.
Powered by Google Gemini REST API (gemini-3.5-flash with automated multi-model fallback).

Features:
1. 📤 Step 1: Resume Parser (PDF, DOCX, TXT extraction + AI structured extraction & ATS audit)
2. 🔍 Step 2: Job Matching (Semantic match scoring & skill gap analysis vs curated corpus or custom JD)
3. ✍️ Step 3: CV Suggestions (Missing keywords, XYZ-format rewritten bullets, tailored summary)
4. 💬 Step 4: AI Career Mentor (Grounded RAG career advisor, mock interview, cover letter generator)
5. 📝 Blog Generator
6. 📧 Email Writer
7. 📄 Resume Builder (Structured manual builder)
8. 📚 History & Analytics
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
    page_title="SmartGen AI — Career Suite & Content Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Minimal Glassmorphism (White + Black)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0a0a0a;
}

/* ── Background ── */
.stApp {
    background: #f5f5f7;
    background-image:
        radial-gradient(ellipse at 15% 10%, rgba(180,200,255,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(200,220,255,0.14) 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-right: 1px solid rgba(0, 0, 0, 0.07);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.04);
}

[data-testid="stSidebar"] * {
    color: #111 !important;
}

/* ── Hero Banner — glass card ── */
.hero-banner {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.8rem;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.05),
        0 1px 0 rgba(255,255,255,0.9) inset;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(60,60,60,0.15), transparent);
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #0a0a0a;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.15;
}

.hero-title span {
    background: linear-gradient(135deg, #111827 0%, #374151 50%, #1f2937 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: rgba(10, 10, 10, 0.6);
    font-size: 1.02rem;
    margin-top: 0.5rem;
    font-weight: 400;
    letter-spacing: -0.01em;
}

/* ── 4-Step Pipeline Flow Diagram (Interactive Visual Indicator) ── */
.pipeline-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0 2rem 0;
}

.pipeline-step {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 18px;
    padding: 1.5rem 1.2rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    position: relative;
    transition: all 0.25s ease;
}

.pipeline-step:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    border-color: rgba(0,0,0,0.15);
}

.step-number {
    position: absolute;
    top: 12px;
    left: 16px;
    font-size: 0.78rem;
    font-weight: 700;
    color: rgba(0,0,0,0.35);
}

.step-icon-circle {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    margin: 0.3rem auto 0.9rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: white;
}

.icon-c1 { background: linear-gradient(135deg, #1e1b4b, #312e81); }
.icon-c2 { background: linear-gradient(135deg, #f87171, #ef4444); }
.icon-c3 { background: linear-gradient(135deg, #10b981, #059669); }
.icon-c4 { background: linear-gradient(135deg, #6366f1, #4f46e5); }

.step-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0a0a0a;
    margin-bottom: 0.35rem;
    letter-spacing: -0.02em;
}

.step-desc {
    font-size: 0.78rem;
    color: rgba(0,0,0,0.55);
    line-height: 1.45;
}

/* ── Glass Cards ── */
.glass-card {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow:
        0 4px 24px rgba(0, 0, 0, 0.05),
        0 1px 0 rgba(255,255,255,0.95) inset;
    margin-bottom: 1.2rem;
}

/* ── Tab Styling ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid rgba(0,0,0,0.07);
    gap: 4px;
}

[data-testid="stTabs"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: rgba(0,0,0,0.5) !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.1rem !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: rgba(255,255,255,0.95) !important;
    color: #0a0a0a !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}

/* ── Input Fields ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 12px !important;
    color: #0a0a0a !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,0,0,0.35) !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06) !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stTextInput label p,
.stNumberInput label p,
.stSlider label p,
.stTextArea label p {
    color: #111111 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: -0.01em !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #0a0a0a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.8rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.16) !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button:hover {
    background: #262626 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.22) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.85) !important;
    color: #0a0a0a !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,255,255,1) !important;
    border-color: rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Output Box ── */
.output-box {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.84rem;
    color: #1a1a1a;
    line-height: 1.75;
    max-height: 520px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.output-box::-webkit-scrollbar { width: 5px; }
.output-box::-webkit-scrollbar-track { background: rgba(0,0,0,0.03); border-radius: 3px; }
.output-box::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 3px; }

/* ── Chips / Tags ── */
.metric-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}

.metric-chip {
    background: rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 20px;
    padding: 0.28rem 0.85rem;
    font-size: 0.78rem;
    color: #222;
    font-weight: 500;
}

.chip-matched {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #065f46;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
}

.chip-missing {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.25);
    color: #991b1b;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.08rem;
    font-weight: 700;
    color: #0a0a0a;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(0,0,0,0.07);
    letter-spacing: -0.02em;
}

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #0a0a0a;
    color: #ffffff;
    font-weight: 800;
    font-size: 1.4rem;
    padding: 0.6rem 1.2rem;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}

/* ── Badges ── */
.badge-success {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.25);
    color: #15803d;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

/* ── Sidebar stats ── */
.sidebar-stat {
    background: rgba(0,0,0,0.04);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 0.7rem 0.95rem;
    margin-bottom: 0.4rem;
    color: #111;
    font-size: 0.86rem;
    font-weight: 500;
}

/* ── Chat Messages ── */
.chat-bubble-user {
    background: #0a0a0a;
    color: #ffffff;
    padding: 0.9rem 1.2rem;
    border-radius: 16px 16px 4px 16px;
    margin: 0.6rem 0 0.6rem auto;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.chat-bubble-ai {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(0,0,0,0.08);
    color: #0a0a0a;
    padding: 1.1rem 1.4rem;
    border-radius: 16px 16px 16px 4px;
    margin: 0.6rem auto 0.6rem 0;
    max-width: 88%;
    font-size: 0.9rem;
    line-height: 1.65;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    border: 1px dashed rgba(0,0,0,0.18);
    border-radius: 16px;
    padding: 1rem;
}

/* ── Divider ── */
hr { border-color: rgba(0,0,0,0.07) !important; }
[data-testid="stHorizontalBlock"] { gap: 1.4rem; }
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
            # Assume plain text or markdown
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
    """
    Calls Google Gemini API using the DIRECT REST API only.
    - Zero SDK overhead (no grpcio, no protobuf warnings)
    - Lightweight, resilient, and includes automated multi-model fallback:
      gemini-3.5-flash → gemini-3.1-flash-lite → gemini-flash-latest → gemini-3.7-flash
    """
    import requests

    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please enter your API key in the sidebar.")

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
                errors.append(f"{m}: Empty response from API")
            else:
                try:
                    err_msg = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    err_msg = resp.text
                errors.append(f"{m} (HTTP {resp.status_code}): {err_msg}")
        except Exception as err:
            errors.append(f"{m}: {err}")

    raise RuntimeError(
        "Gemini API call failed. Please check your API key.\n\nDetails:\n"
        + "\n".join(errors[-4:])
    )


# ─────────────────────────────────────────────
# AI Pipeline Functions
# ─────────────────────────────────────────────

def parse_resume_with_ai(resume_text: str, api_key: str, model: str = "gemini-3.5-flash") -> dict:
    """
    Step 1: Parse raw resume text into validated, structured profile:
    skills, experience, education, target role, and ATS score.
    """
    system_instruction = (
        "You are an expert Resume Parser and ATS Auditor. "
        "You must analyze the candidate's resume and return ONLY a valid JSON object matching the exact schema."
    )
    prompt = f"""Extract and structure all information from this resume into the JSON format below.

Resume Text:
\"\"\"{resume_text[:6000]}\"\"\"

Respond ONLY with valid JSON in this exact structure (no extra commentary, no markdown codeblocks):
{{
  "name": "Candidate Full Name or Unknown",
  "target_role": "Inferred or stated Target Role",
  "contact": {{
    "email": "email or not found",
    "phone": "phone or not found",
    "location": "location or not found"
  }},
  "ats_score": 85,
  "summary": "3-sentence professional summary extracted or synthesized from the resume.",
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
      "highlights": ["Key quantified achievement 1", "Key achievement 2"]
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "University / College",
      "year": "Year"
    }}
  ],
  "strengths": ["Key candidate strength 1", "Strength 2"],
  "ats_improvements": ["Specific improvement 1 to boost ATS parsing", "Improvement 2"]
}}
"""
    raw_response = call_gemini(system_instruction, prompt, temperature=0.1, api_key=api_key, model=model)

    # Clean JSON output if wrapped in markdown
    clean_json = raw_response
    if "```json" in clean_json:
        clean_json = clean_json.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_json:
        clean_json = clean_json.split("```")[1].split("```")[0].strip()

    try:
        parsed_data = json.loads(clean_json)
        return parsed_data
    except Exception:
        # Fallback structured object
        return {
            "name": "Parsed Candidate",
            "target_role": "Software Professional",
            "contact": {"email": "Extracted from resume", "phone": "N/A", "location": "N/A"},
            "ats_score": 78,
            "summary": clean_json[:300],
            "skills": {
                "core_technical": ["Python", "Problem Solving", "Data Structures"],
                "frameworks_tools": ["Git", "REST APIs"],
                "soft_skills": ["Teamwork", "Communication"]
            },
            "experience": [{"role": "Professional Experience", "company": "Experience Mentioned", "duration": "Recent", "highlights": [clean_json[:200]]}],
            "education": [{"degree": "Higher Education", "institution": "University", "year": "Recent"}],
            "strengths": ["Hands-on project experience"],
            "ats_improvements": ["Quantify achievements with metrics (%, $, time saved)."]
        }


# Default Curated Job Corpus
DEFAULT_JOB_CORPUS = [
    {
        "id": "job_1",
        "title": "Senior Generative AI / LLM Engineer",
        "company": "Anthropic / Tech Ecosystem",
        "domain": "AI / ML",
        "skills_required": ["Python", "Google Gemini API", "LLMs", "RAG", "Prompt Engineering", "Vector DBs", "FastAPI", "PyTorch", "Docker"],
        "description": "Build high-throughput RAG systems, integrate multi-modal LLM APIs, optimize prompts, and develop end-to-end AI applications."
    },
    {
        "id": "job_2",
        "title": "Full Stack Developer (Python & React)",
        "company": "CloudScale Solutions",
        "domain": "Web Development",
        "skills_required": ["Python", "React", "TypeScript", "FastAPI", "PostgreSQL", "REST APIs", "Docker", "Git", "Tailwind CSS"],
        "description": "Design responsive web applications, construct high-performance RESTful APIs, manage relational databases, and lead frontend/backend integrations."
    },
    {
        "id": "job_3",
        "title": "Data Scientist & Machine Learning Specialist",
        "company": "Apex Analytics",
        "domain": "Data Science",
        "skills_required": ["Python", "SQL", "Pandas", "Scikit-Learn", "TensorFlow", "Data Visualization", "Statistical Analysis", "Machine Learning"],
        "description": "Analyze large datasets, develop predictive models, uncover key business insights, and deploy machine learning models in production."
    },
    {
        "id": "job_4",
        "title": "Cloud DevOps & Infrastructure Architect",
        "company": "Nebula Cloud Systems",
        "domain": "Cloud & DevOps",
        "skills_required": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux", "Python", "Monitoring", "Security"],
        "description": "Maintain cloud infrastructure, automate deployment pipelines, implement observability and infrastructure-as-code."
    },
    {
        "id": "job_5",
        "title": "Frontend Engineer (React / Next.js)",
        "company": "Vivid Interface Labs",
        "domain": "Frontend",
        "skills_required": ["React", "Next.js", "JavaScript", "TypeScript", "CSS / Glassmorphism", "REST APIs", "UI/UX Design", "Git"],
        "description": "Craft stunning, high-performance web user interfaces with modern glassmorphism design, fluid animations, and robust client-side state management."
    }
]


def match_resume_to_jobs(parsed_profile: dict, job_list: list, api_key: str, model: str = "gemini-3.5-flash") -> list:
    """
    Step 2: Match candidate profile against job corpus and compute match scores & skill gaps.
    """
    profile_summary = f"""
Candidate Target Role: {parsed_profile.get('target_role', '')}
Skills: {json.dumps(parsed_profile.get('skills', {}))}
Summary: {parsed_profile.get('summary', '')}
"""
    jobs_summary = json.dumps([{
        "id": j["id"],
        "title": j["title"],
        "company": j["company"],
        "skills_required": j["skills_required"]
    } for j in job_list])

    system_instruction = (
        "You are an AI Talent Matcher. Calculate the semantic match score (0-100%) between a candidate's profile "
        "and each job posting. Return ONLY a JSON list of matches."
    )
    prompt = f"""Compare this candidate profile with the jobs list.

Candidate Profile:
{profile_summary}

Jobs List:
{jobs_summary}

Respond ONLY with valid JSON array:
[
  {{
    "id": "job_id",
    "match_score": 88,
    "matched_skills": ["Skill 1", "Skill 2"],
    "missing_skills": ["Skill 3", "Skill 4"],
    "fit_summary": "Brief 1-sentence assessment of candidate's fit."
  }}
]
"""
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
            # Fallback simple matching
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
    """
    Step 3: AI-generated missing skills, rewritten bullet points (XYZ format), and a summary tailored to a chosen job.
    """
    system_instruction = (
        "You are an Elite Executive Resume Strategist & Career Coach. "
        "Provide actionable, high-impact CV optimization tailored specifically to the chosen job posting."
    )
    prompt = f"""Generate tailored CV suggestions and an optimized resume section for this candidate applying to the target job.

Candidate Profile:
{json.dumps(parsed_profile, indent=2)}

Target Job:
Role: {target_job.get('title')} at {target_job.get('company')}
Required Skills: {', '.join(target_job.get('skills_required', []))}
Job Description: {target_job.get('description', '')}

Structure your response with clear sections using '━━━' dividers:

1. 🎯 TARGETED PROFESSIONAL SUMMARY
Provide a polished 3-4 sentence summary customized for the {target_job.get('title')} role that highlights key strengths.

2. 🔑 MISSING KEYWORDS & SKILLS TO INJECT
List the exact high-value keywords and tools the candidate must add to pass ATS filters for this role.

3. ⚡ HIGH-IMPACT BULLET POINT REWRITES (XYZ FORMAT)
Take 3 weak/generic bullets from their experience and rewrite them in Google's XYZ formula:
'Accomplished [X] as measured by [Y], by doing [Z]'
Show:
• Before: [original/generic]
• After: [impactful, quantified, keyword-rich rewrite]

4. 📋 ATS COMPLIANCE & WEAKNESS AUDIT
Provide 3 specific suggestions to maximize ATS readability and interview callback probability.

5. 📄 FULL TAILORED RESUME PREVIEW
Provide a clean, ready-to-copy tailored resume text formatted with clear sections.
"""
    return call_gemini(system_instruction, prompt, temperature=0.3, api_key=api_key, model=model)


def career_mentor_chat(messages: list, candidate_context: str, job_context: str, api_key: str, model: str = "gemini-3.5-flash") -> str:
    """
    Step 4: A grounded RAG career mentor chatbot grounded in the user's resume & target job postings.
    """
    system_instruction = f"""You are 'SmartGen AI Career Mentor' — an elite executive career advisor, interview coach, and talent strategist.
You are grounded in the user's resume and their target job posting.

Candidate Resume Context:
{candidate_context}

Target Job Context:
{job_context}

Guidelines:
- Provide actionable, direct, and encouraging career coaching.
- Generate realistic mock interview questions & STAR-method answer frameworks when asked.
- Provide step-by-step 30/60/90-day learning roadmaps to bridge skill gaps.
- Craft targeted cover letters and cold outreach messages.
- Maintain professional tone and adhere to safety guardrails (only provide ethical, legitimate career and interview advice).
"""
    # Build chat transcript prompt
    chat_history_str = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "AI Mentor"
        chat_history_str += f"{role}: {msg['content']}\n\n"

    last_user_msg = messages[-1]["content"] if messages else "Hello! How can you help my career?"
    prompt = f"Conversation History:\n{chat_history_str}\n\nProvide a comprehensive, insightful mentor response to the user's latest query."

    return call_gemini(system_instruction, prompt, temperature=0.5, api_key=api_key, model=model)


# Standard Blog, Email & Resume functions
def generate_blog(topic: str, tone: str, word_count: int, api_key: str, model: str = "gemini-3.5-flash") -> str:
    system_instruction = "You are an experienced blog writer who crafts engaging, insightful, and well-structured articles."
    prompt = f"""Write a blog post based on the following details:
- Topic: "{topic}"
- Tone: {tone}
- Target Word Count: {word_count} words

Formatting & Structure Guidelines:
1. Title: Create an engaging, catchy title.
2. Intro Hook: Start with a strong hook that captures reader interest.
3. Body Sections: Write 2 to 3 distinct body sections with descriptive subheadings.
4. Conclusion: Summarize main points with a memorable takeaway or call to action.
"""
    return call_gemini(system_instruction, prompt, temperature=0.7, api_key=api_key, model=model)


def generate_email(recipient: str, purpose: str, tone: str, api_key: str, model: str = "gemini-3.5-flash") -> str:
    system_instruction = "You are a professional email writer who produces clear, polished, and effective emails."
    prompt = f"""Write an email based on the following details:
- Recipient: {recipient}
- Purpose: {purpose}
- Tone: {tone}

Formatting & Structure Guidelines:
1. Subject Line: Clear and professional subject line.
2. Salutation: Appropriate greeting to {recipient}.
3. Email Body: Concise, context-appropriate message addressing the purpose ({purpose}).
4. Closing: Professional sign-off with placeholders for sender details.
"""
    return call_gemini(system_instruction, prompt, temperature=0.3, api_key=api_key, model=model)


def generate_resume(
    name: str, job_title: str, email: str, phone: str, location: str,
    summary: str, experience: str, education: str, skills: str,
    projects: str, certifications: str, api_key: str, model: str = "gemini-3.5-flash"
) -> str:
    system_instruction = (
        "You are an expert resume writer with 15+ years of experience crafting "
        "ATS-optimised, professional resumes for top companies. You write with "
        "impact — using strong action verbs, quantified achievements, and clean formatting."
    )
    prompt = f"""Build a polished, ATS-friendly professional resume using the details below.

Candidate Details:
- Full Name: {name}
- Target Role: {job_title}
- Email: {email}
- Phone: {phone}
- Location: {location}

Professional Summary Input: {summary}

Work Experience:
{experience}

Education:
{education}

Skills: {skills}

Projects: {projects}

Certifications: {certifications}

Formatting Rules:
1. Header — Name (large), contact line (email | phone | location).
2. Professional Summary — 3-4 compelling sentences tailored to the target role.
3. Work Experience — reverse-chronological, bullet points with strong action verbs and metrics.
4. Education — degree, institution, year.
5. Skills — grouped by category (Technical, Soft Skills, Tools).
6. Projects — name, brief description, tech stack.
7. Certifications — name, issuer, year.
Output plain text only. Use ━━━ as section dividers. Keep it concise (1–2 pages).
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
        {"role": "assistant", "content": "👋 Hi there! I'm your **AI Career Mentor**. Upload your resume or select a target job to get started with tailored interview prep, skill roadmap, or cover letter generation!"}
    ]
if "total_generated" not in st.session_state:
    st.session_state.total_generated = 0


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 1.6rem;">
        <div style="font-size:2rem; margin-bottom:0.4rem;">✦</div>
        <div style="font-size:1.25rem; font-weight:800; color:#0a0a0a; letter-spacing:-0.03em;">SmartGen AI</div>
        <div style="color:rgba(0,0,0,0.45); font-size:0.75rem; margin-top:0.25rem; font-weight:500;">
            Career Intelligence & Content Studio
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🔑 API Configuration**")
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
        placeholder="Paste your API key here…",
        help="Get your free key at https://aistudio.google.com/apikey",
    )

    model_choice = st.selectbox(
        "Gemini Model",
        options=["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.7-flash"],
        index=0,
        help="Default: gemini-3.5-flash (fastest & highest quality for new API keys)",
    )

    if api_key:
        st.markdown('<div class="badge-success">✓ API Key ready</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Enter your API Key to start generating.")

    st.divider()

    st.markdown("**📊 Session Stats**")
    has_profile = "✓ Active" if st.session_state.parsed_profile else "None"
    st.markdown(f"""
    <div class="sidebar-stat">👤 Resume Profile: <strong>{has_profile}</strong></div>
    <div class="sidebar-stat">🎯 Matched Job: <strong>{st.session_state.selected_job['title'][:18] + '...' if st.session_state.selected_job else 'None'}</strong></div>
    <div class="sidebar-stat">📝 Blogs Generated: <strong>{len(st.session_state.blog_history)}</strong></div>
    <div class="sidebar-stat">📧 Emails Generated: <strong>{len(st.session_state.email_history)}</strong></div>
    <div class="sidebar-stat">📄 Resumes Built: <strong>{len(st.session_state.resume_history)}</strong></div>
    <div class="sidebar-stat">⚡ Total Operations: <strong>{st.session_state.total_generated}</strong></div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="color:rgba(0,0,0,0.45); font-size:0.8rem; line-height:1.7;">
    SmartGen AI integrates Gemini to empower your career & content.<br><br>
    🚀 <strong style="color:#111;">4-Step Pipeline:</strong> Parser ➔ Matcher ➔ Suggestions ➔ Mentor<br><br>
    <a href="https://aistudio.google.com/apikey" target="_blank"
       style="color:#0a0a0a; font-weight:600; text-decoration:none;">
       → Get your free API key
    </a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title"><span>✦ SmartGen AI</span></div>
    <div class="hero-subtitle">
        AI-Powered Career &amp; Content Intelligence Studio —
        Parse Resumes, Match Jobs, Optimize CVs &amp; Elevate Your Career.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4-Step Pipeline Flow (Visual Diagram)
# ─────────────────────────────────────────────
st.markdown("""
<div class="pipeline-container">
    <div class="pipeline-step">
        <span class="step-number">1</span>
        <div class="step-icon-circle icon-c1">📤</div>
        <div class="step-title">Resume Parser</div>
        <div class="step-desc">Upload PDF/DOCX to extract structured skills, experience & ATS score.</div>
    </div>
    <div class="pipeline-step">
        <span class="step-number">2</span>
        <div class="step-icon-circle icon-c2">🔍</div>
        <div class="step-title">Job Matching</div>
        <div class="step-desc">Semantic search returns top matching postings with score & skill gap analysis.</div>
    </div>
    <div class="pipeline-step">
        <span class="step-number">3</span>
        <div class="step-icon-circle icon-c3">✍️</div>
        <div class="step-title">CV Suggestions</div>
        <div class="step-desc">AI-generated missing skills, XYZ bullet rewrites, and tailored summaries.</div>
    </div>
    <div class="pipeline-step">
        <span class="step-number">4</span>
        <div class="step-icon-circle icon-c4">💬</div>
        <div class="step-title">AI Career Mentor</div>
        <div class="step-desc">A RAG career advisor for mock interviews, roadmaps, and cover letters.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Main Tabs Navigation
# ─────────────────────────────────────────────
tab_career, tab_blog, tab_email, tab_resume_builder, tab_history = st.tabs([
    "🚀  AI Career Suite",
    "📝  Blog Generator",
    "📧  Email Writer",
    "📄  Resume Builder",
    "📚  History & Analytics",
])


# ══════════════════════════════════════════════
# TAB 1 — AI CAREER SUITE (4-STEP PROGRESSIVE PIPELINE)
# ══════════════════════════════════════════════
with tab_career:
    st.markdown('<div class="section-header">🎯 AI Career Intelligence Suite</div>', unsafe_allow_html=True)

    career_step = st.radio(
        "Pipeline Workflow Navigation:",
        options=[
            "Step 1: 📤 Resume Parser",
            "Step 2: 🔍 Job Matching & Gap Analysis",
            "Step 3: ✍️ CV Suggestions & Tailoring",
            "Step 4: 💬 AI Career Mentor (Chatbot)",
        ],
        horizontal=True,
        key="career_pipeline_step"
    )

    st.markdown("---")

    # ──────────────────────────────────────────
    # STEP 1: RESUME PARSER
    # ──────────────────────────────────────────
    if "Step 1" in career_step:
        col_upload, col_profile = st.columns([1, 1], gap="large")

        with col_upload:
            st.markdown('<div class="section-header">📤 Upload or Paste Resume</div>', unsafe_allow_html=True)

            upload_mode = st.radio("Input Format:", ["Upload Document (PDF, DOCX, TXT)", "Paste Raw Text"], horizontal=True)

            resume_content = ""
            if upload_mode == "Upload Document (PDF, DOCX, TXT)":
                uploaded_file = st.file_uploader(
                    "Choose a resume file",
                    type=["pdf", "docx", "txt"],
                    help="Supports .pdf, .docx, and .txt formats."
                )
                if uploaded_file:
                    try:
                        resume_content = extract_text_from_file(uploaded_file)
                        st.success(f"✓ Extracted {len(resume_content.split())} words from **{uploaded_file.name}**")
                        with st.expander("Preview Extracted Raw Text"):
                            st.text(resume_content[:1000] + ("..." if len(resume_content) > 1000 else ""))
                    except Exception as e:
                        st.error(f"❌ {e}")
            else:
                resume_content = st.text_area(
                    "Paste Resume Content Here:",
                    placeholder="Paste full text of your resume including contact, skills, experience, and education...",
                    height=260
                )

            parse_btn = st.button("✦ Parse & Audit Resume with AI", use_container_width=True, key="parse_resume_btn")

            if parse_btn:
                if not api_key:
                    st.error("❌ Please enter your Gemini API Key in the sidebar.")
                elif not resume_content.strip():
                    st.warning("⚠️ Please upload a resume file or paste resume text.")
                else:
                    with st.spinner("Analyzing resume structure, skills, and ATS score…"):
                        try:
                            start = time.time()
                            parsed = parse_resume_with_ai(resume_content, api_key=api_key, model=model_choice)
                            elapsed = round(time.time() - start, 1)

                            st.session_state.parsed_profile = parsed
                            st.session_state.raw_resume_text = resume_content
                            st.session_state.total_generated += 1
                            st.success(f"✓ Resume successfully parsed in {elapsed}s!")
                        except Exception as e:
                            st.error(f"❌ Error parsing resume: {e}")

        with col_profile:
            st.markdown('<div class="section-header">👤 Validated Candidate Profile & ATS Score</div>', unsafe_allow_html=True)

            profile = st.session_state.parsed_profile
            if profile:
                # Top ATS score card
                ats_score = profile.get("ats_score", 80)
                col_score, col_meta = st.columns([1, 2])
                with col_score:
                    st.markdown(f"""
                    <div style="text-align:center; padding:1.2rem; background:rgba(0,0,0,0.03); border-radius:18px; border:1px solid rgba(0,0,0,0.08);">
                        <div style="font-size:0.75rem; color:rgba(0,0,0,0.5); font-weight:700; text-transform:uppercase;">ATS Readiness</div>
                        <div class="score-badge" style="margin-top:0.4rem;">{ats_score}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_meta:
                    st.markdown(f"""
                    <div style="padding:0.4rem 0;">
                        <div style="font-size:1.35rem; font-weight:800; color:#0a0a0a;">{profile.get('name', 'Candidate')}</div>
                        <div style="font-size:0.95rem; font-weight:600; color:#4b5563;">🎯 {profile.get('target_role', 'Not Specified')}</div>
                        <div style="font-size:0.82rem; color:#6b7280; margin-top:0.3rem;">
                            📍 {profile.get('contact', {}).get('location', 'N/A')} &nbsp;|&nbsp; ✉️ {profile.get('contact', {}).get('email', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Summary
                st.markdown("**✍ Professional Summary**")
                st.markdown(f"""<div style="font-size:0.88rem; color:#374151; line-height:1.6; background:rgba(255,255,255,0.7); padding:0.9rem; border-radius:12px; border:1px solid rgba(0,0,0,0.06);">{profile.get('summary', 'No summary generated.')}</div>""", unsafe_allow_html=True)

                # Skills breakdown
                st.markdown("**⚡ Extracted & Categorized Skills**")
                skills_data = profile.get("skills", {})
                if isinstance(skills_data, dict):
                    for cat, s_list in skills_data.items():
                        cat_title = cat.replace("_", " ").title()
                        st.markdown(f"<span style='font-size:0.8rem; font-weight:700; color:#4b5563;'>{cat_title}:</span>", unsafe_allow_html=True)
                        chips_html = "".join([f"<span class='metric-chip' style='margin:2px;'>{s}</span>" for s in s_list])
                        st.markdown(f"<div style='margin-bottom:0.6rem;'>{chips_html}</div>", unsafe_allow_html=True)

                # Experience Highlights
                st.markdown("**💼 Work History Highlights**")
                for exp in profile.get("experience", []):
                    with st.expander(f"📌 {exp.get('role', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'Dates')})"):
                        for hl in exp.get("highlights", []):
                            st.markdown(f"• {hl}")

                # ATS Improvements
                if profile.get("ats_improvements"):
                    st.markdown("**💡 ATS Optimization Tips**")
                    for tip in profile.get("ats_improvements", []):
                        st.markdown(f"• {tip}")

                st.info("👉 Profile loaded! Navigate to **Step 2: Job Matching** above to find tailored postings.")
            else:
                st.markdown("""
                <div style="text-align:center; padding:4rem 2rem; color:rgba(0,0,0,0.3);">
                    <div style="font-size:2.8rem; margin-bottom:0.6rem;">📄</div>
                    <div style="font-size:0.95rem; font-weight:600;">No Resume Parsed Yet</div>
                    <div style="font-size:0.82rem; margin-top:0.3rem;">Upload your PDF/DOCX or paste text on the left to extract your profile.</div>
                </div>
                """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # STEP 2: JOB MATCHING & GAP ANALYSIS
    # ──────────────────────────────────────────
    elif "Step 2" in career_step:
        st.markdown('<div class="section-header">🔍 Semantic Job Matching & Skill Gap Analysis</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("⚠️ Please parse your resume in **Step 1** first so we can match your profile against jobs.")
        else:
            col_cfg, col_jobs = st.columns([1, 2], gap="large")

            with col_cfg:
                st.markdown("**📋 Job Search Configuration**")
                job_source = st.radio(
                    "Job Corpus Source:",
                    ["Use Built-in High-Demand Job Corpus", "Add / Paste Custom Job Description"],
                    key="job_source_mode"
                )

                active_jobs = list(DEFAULT_JOB_CORPUS)
                if job_source == "Add / Paste Custom Job Description":
                    c_title = st.text_input("Job Title", placeholder="e.g. AI Product Engineer", value="AI Product Engineer")
                    c_company = st.text_input("Company", placeholder="e.g. Acme AI Labs", value="Acme AI Labs")
                    c_skills = st.text_input("Required Skills (comma-separated)", value="Python, Gemini API, RAG, Streamlit, Git, Docker")
                    c_desc = st.text_area("Job Description", placeholder="Paste the complete JD here...", height=150, value="We are looking for an AI Engineer to build intelligent web apps with Gemini LLM APIs, vector search, and clean user interfaces.")

                    custom_job = {
                        "id": "custom_job_1",
                        "title": c_title,
                        "company": c_company,
                        "domain": "Custom Target",
                        "skills_required": [s.strip() for s in c_skills.split(",") if s.strip()],
                        "description": c_desc
                    }
                    active_jobs = [custom_job] + DEFAULT_JOB_CORPUS

                match_btn = st.button("✦ Run Semantic Match & Gap Analysis", use_container_width=True, key="run_match_btn")

            with col_jobs:
                st.markdown("**🎯 Matching Results & Score Breakdown**")

                if match_btn or "matched_jobs_list" in st.session_state:
                    if match_btn:
                        if not api_key:
                            st.error("❌ Please enter your Gemini API Key in the sidebar.")
                        else:
                            with st.spinner("Computing semantic match scores and skill gaps…"):
                                try:
                                    matched_results = match_resume_to_jobs(
                                        st.session_state.parsed_profile,
                                        active_jobs,
                                        api_key=api_key,
                                        model=model_choice
                                    )
                                    st.session_state.matched_jobs_list = matched_results
                                    st.session_state.total_generated += 1
                                except Exception as e:
                                    st.error(f"❌ Matching error: {e}")

                    matched_jobs = st.session_state.get("matched_jobs_list", [])
                    if matched_jobs:
                        for idx, job in enumerate(matched_jobs):
                            score = job.get("match_score", 70)
                            color_style = "#15803d" if score >= 80 else "#b45309" if score >= 60 else "#b91c1c"

                            with st.container():
                                st.markdown(f"""
                                <div class="glass-card" style="padding:1.4rem; margin-bottom:1rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <div>
                                            <div style="font-size:1.15rem; font-weight:800; color:#0a0a0a;">{job['title']}</div>
                                            <div style="font-size:0.88rem; color:#4b5563; font-weight:600;">🏢 {job['company']} &nbsp;|&nbsp; 🏷️ {job.get('domain', 'Tech')}</div>
                                        </div>
                                        <div style="text-align:right;">
                                            <span style="background:{color_style}; color:white; font-weight:800; font-size:1.1rem; padding:0.4rem 0.9rem; border-radius:14px;">
                                                {score}% Match
                                            </span>
                                        </div>
                                    </div>
                                    <div style="margin-top:0.8rem; font-size:0.84rem; color:#374151;">
                                        {job.get('fit_summary', job.get('description', '')[:140])}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                col_m, col_g, col_act = st.columns([1, 1, 0.8])
                                with col_m:
                                    st.markdown("<span style='font-size:0.78rem; font-weight:700; color:#15803d;'>✅ Matched Skills:</span>", unsafe_allow_html=True)
                                    matched_chips = "".join([f"<span class='chip-matched'>{s}</span>" for s in job.get("matched_skills", [])]) or "<span style='font-size:0.75rem; color:#6b7280;'>None identified</span>"
                                    st.markdown(matched_chips, unsafe_allow_html=True)
                                with col_g:
                                    st.markdown("<span style='font-size:0.78rem; font-weight:700; color:#b91c1c;'>⚠️ Missing Skills to Target:</span>", unsafe_allow_html=True)
                                    missing_chips = "".join([f"<span class='chip-missing'>{s}</span>" for s in job.get("missing_skills", [])]) or "<span style='font-size:0.75rem; color:#15803d;'>Zero skill gaps!</span>"
                                    st.markdown(missing_chips, unsafe_allow_html=True)
                                with col_act:
                                    if st.button(f"🎯 Target This Job", key=f"select_job_{job['id']}_{idx}"):
                                        st.session_state.selected_job = job
                                        st.success(f"✓ Selected: **{job['title']}**! Proceed to Step 3 or 4.")
                                st.markdown("---")
                    else:
                        st.info("Click **Run Semantic Match & Gap Analysis** to score your profile.")
                else:
                    st.info("Click **Run Semantic Match & Gap Analysis** on the left to evaluate matches.")

    # ──────────────────────────────────────────
    # STEP 3: CV SUGGESTIONS & TAILORING
    # ──────────────────────────────────────────
    elif "Step 3" in career_step:
        st.markdown('<div class="section-header">✍️ AI CV Suggestions & Bullet Rewriter</div>', unsafe_allow_html=True)

        if not st.session_state.parsed_profile:
            st.warning("⚠️ Please parse your resume in **Step 1** first.")
        else:
            col_target, col_out = st.columns([1, 1.4], gap="large")

            with col_target:
                st.markdown("**🎯 Selected Target Job**")

                # Allow picking from matched or creating custom
                job_options = [j["title"] + f" ({j['company']})" for j in DEFAULT_JOB_CORPUS]
                sel_idx = 0
                if st.session_state.selected_job:
                    cur_title = st.session_state.selected_job["title"]
                    for i, opt in enumerate(job_options):
                        if cur_title in opt:
                            sel_idx = i
                            break

                chosen_opt = st.selectbox("Choose Target Job Role:", job_options, index=sel_idx)
                selected_job_obj = DEFAULT_JOB_CORPUS[0]
                for j in DEFAULT_JOB_CORPUS:
                    if j["title"] in chosen_opt:
                        selected_job_obj = j
                        break

                if st.session_state.selected_job:
                    selected_job_obj = st.session_state.selected_job

                st.markdown(f"""
                <div class="glass-card" style="padding:1.2rem; margin-top:0.6rem;">
                    <div style="font-weight:700; font-size:1.05rem;">{selected_job_obj['title']}</div>
                    <div style="color:#4b5563; font-size:0.85rem; margin-top:0.2rem;">🏢 {selected_job_obj['company']}</div>
                    <div style="margin-top:0.6rem; font-size:0.8rem; color:#374151;">
                        <strong>Key Requirements:</strong> {', '.join(selected_job_obj.get('skills_required', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                generate_sugg_btn = st.button("✦ Generate Tailored CV Suggestions", use_container_width=True, key="gen_cv_sugg_btn")

            with col_out:
                st.markdown('<div class="section-header">📋 AI Optimization Plan & Rewritten Resume</div>', unsafe_allow_html=True)

                if generate_sugg_btn:
                    if not api_key:
                        st.error("❌ Please enter your Gemini API Key in the sidebar.")
                    else:
                        with st.spinner("Tailoring CV, rewriting bullet points, and synthesizing keywords…"):
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
                                st.success(f"✓ Suggestions generated in {elapsed}s!")
                            except Exception as e:
                                st.error(f"❌ Error: {e}")

                if st.session_state.cv_suggestions_output:
                    output_text = st.session_state.cv_suggestions_output
                    st.markdown(f'<div class="output-box">{output_text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Download Tailored_CV_Optimization.txt",
                        data=output_text,
                        file_name=f"Tailored_{selected_job_obj['title'].replace(' ', '_')}_CV.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                else:
                    st.markdown("""
                    <div style="text-align:center; padding:3.5rem 2rem; color:rgba(0,0,0,0.3);">
                        <div style="font-size:2.8rem; margin-bottom:0.6rem;">✍️</div>
                        <div style="font-size:0.92rem; font-weight:600;">Ready to Tailor Your CV</div>
                        <div style="font-size:0.82rem; margin-top:0.3rem;">Select your target job on the left and click Generate to see XYZ bullet rewrites and missing keywords.</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # STEP 4: AI CAREER MENTOR (RAG CHATBOT)
    # ──────────────────────────────────────────
    elif "Step 4" in career_step:
        st.markdown('<div class="section-header">💬 AI Career Mentor — Grounded Coaching & Interview Prep</div>', unsafe_allow_html=True)

        col_chat_cfg, col_chat_main = st.columns([1, 2.2], gap="large")

        with col_chat_cfg:
            st.markdown("**🎯 Grounded Context**")
            profile_ctx = "No resume uploaded yet"
            if st.session_state.parsed_profile:
                p = st.session_state.parsed_profile
                profile_ctx = f"Candidate: {p.get('name')} | Role: {p.get('target_role')} | Skills: {p.get('skills')}"

            job_ctx = "General Tech Industry"
            if st.session_state.selected_job:
                j = st.session_state.selected_job
                job_ctx = f"Target Role: {j.get('title')} at {j.get('company')} | Required: {j.get('skills_required')}"

            st.markdown(f"""
            <div class="sidebar-stat" style="font-size:0.8rem; line-height:1.5;">
                <strong>Candidate:</strong><br>{profile_ctx[:120]}...<br><br>
                <strong>Target Job:</strong><br>{job_ctx[:120]}...
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**⚡ Quick Mentor Prompts**")
            q1 = st.button("🎯 Mock Interview Questions", use_container_width=True)
            q2 = st.button("💡 60-Day Upskilling Roadmap", use_container_width=True)
            q3 = st.button("✉️ Draft Targeted Cover Letter", use_container_width=True)
            q4 = st.button("📈 Salary Negotiation Script", use_container_width=True)

            auto_prompt = None
            if q1:
                auto_prompt = "Generate 5 challenging technical and behavioral interview questions tailored to my resume and target role, along with model answers using the STAR method."
            elif q2:
                auto_prompt = "Create a structured 60-day step-by-step learning roadmap with project milestones to bridge my missing skills for this target role."
            elif q3:
                auto_prompt = "Write a compelling, professional cover letter tailored to this target job posting highlighting my strongest relevant achievements."
            elif q4:
                auto_prompt = "Provide a salary negotiation script and benchmark strategy for this role based on current market standards."

            if st.button("🗑 Reset Chat History", use_container_width=True):
                st.session_state.mentor_messages = [
                    {"role": "assistant", "content": "👋 Chat reset. What would you like to discuss next?"}
                ]
                st.rerun()

        with col_chat_main:
            # Display Chat History
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.mentor_messages:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

            user_input = st.chat_input("Ask your Career Mentor a question (interview prep, skill roadmap, cover letter)...")
            final_input = auto_prompt or user_input

            if final_input:
                if not api_key:
                    st.error("❌ Please enter your Gemini API Key in the sidebar.")
                else:
                    st.session_state.mentor_messages.append({"role": "user", "content": final_input})
                    st.markdown(f'<div class="chat-bubble-user">{final_input}</div>', unsafe_allow_html=True)

                    with st.spinner("AI Mentor is thinking…"):
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
                            st.error(f"❌ Error: {e}")


# ══════════════════════════════════════════════
# TAB 2 — BLOG GENERATOR
# ══════════════════════════════════════════════
with tab_blog:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">⚙️ Blog Configuration</div>', unsafe_allow_html=True)

        topic = st.text_input(
            "Blog Topic",
            placeholder="e.g. Why Python is the best first language",
            value="Why Python is the best first language",
            help="Enter the topic you want to write about.",
        )

        tone = st.selectbox(
            "Writing Tone",
            options=["casual", "professional", "formal", "Gen Z", "humorous", "inspirational"],
            index=0,
            help="The tone sets the personality and style of the blog.",
        )

        word_count = st.slider(
            "Target Word Count",
            min_value=100,
            max_value=1500,
            value=300,
            step=50,
            help="Approximate word count for the blog post.",
        )

        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-chip">🌡 Temp: 0.7</span>
            <span class="metric-chip">📏 ~{word_count} words</span>
            <span class="metric-chip">🎨 {tone}</span>
        </div>
        """, unsafe_allow_html=True)

        generate_blog_btn = st.button("✦ Generate Blog Post", use_container_width=True, key="gen_blog")

    with col_right:
        st.markdown('<div class="section-header">📄 Generated Blog</div>', unsafe_allow_html=True)

        if generate_blog_btn:
            if not api_key:
                st.error("❌ Please enter your Gemini API Key in the sidebar.")
            elif not topic.strip():
                st.warning("⚠️ Please enter a blog topic.")
            else:
                with st.spinner("Generating your blog post…"):
                    try:
                        start = time.time()
                        blog_text = generate_blog(topic, tone, word_count, api_key, model=model_choice)
                        elapsed = round(time.time() - start, 1)

                        header = f"===== BLOG GENERATOR =====\nTopic: \"{topic}\"\nTone: {tone}\nWord count: {word_count}\n\n"
                        full_output = header + blog_text

                        st.session_state.blog_history.append({
                            "topic": topic,
                            "tone": tone,
                            "word_count": word_count,
                            "output": full_output,
                        })
                        st.session_state.total_generated += 1

                        st.success(f"✓ Generated in {elapsed}s")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "⬇ Download blog_output.txt",
                            data=full_output,
                            file_name="blog_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"❌ {e}")

        elif st.session_state.blog_history:
            last = st.session_state.blog_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇ Download blog_output.txt",
                data=last["output"],
                file_name="blog_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:rgba(0,0,0,0.25);">
                <div style="font-size:2.5rem; margin-bottom:0.6rem;">📝</div>
                <div style="font-size:0.9rem; font-weight:500;">
                    Configure and click <strong style="color:rgba(0,0,0,0.4);">Generate</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — EMAIL WRITER
# ══════════════════════════════════════════════
with tab_email:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">⚙️ Email Configuration</div>', unsafe_allow_html=True)

        recipient = st.text_input(
            "Recipient Name / Role",
            placeholder="e.g. HR Manager, TCS",
            value="HR Manager, TCS",
            help="Who is this email addressed to?",
        )

        purpose = st.selectbox(
            "Email Purpose",
            options=[
                "Follow-up after interview",
                "Cold outreach",
                "Thank-you note",
                "Leave request",
                "Project update",
                "Meeting request",
                "Custom…",
            ],
            index=0,
        )

        if purpose == "Custom…":
            purpose = st.text_input("Describe the email purpose:", placeholder="e.g. Requesting project extension")

        email_tone = st.selectbox(
            "Email Tone",
            options=["professional", "formal", "friendly", "casual", "assertive"],
            index=0,
        )

        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-chip">🌡 Temp: 0.3</span>
            <span class="metric-chip">✍ {email_tone}</span>
        </div>
        """, unsafe_allow_html=True)

        generate_email_btn = st.button("✦ Generate Email", use_container_width=True, key="gen_email")

    with col_right:
        st.markdown('<div class="section-header">📄 Generated Email</div>', unsafe_allow_html=True)

        if generate_email_btn:
            if not api_key:
                st.error("❌ Please enter your Gemini API Key in the sidebar.")
            elif not recipient.strip():
                st.warning("⚠️ Please enter a recipient.")
            elif not purpose or not purpose.strip():
                st.warning("⚠️ Please describe the email purpose.")
            else:
                with st.spinner("Composing your email…"):
                    try:
                        start = time.time()
                        email_text = generate_email(recipient, purpose, email_tone, api_key, model=model_choice)
                        elapsed = round(time.time() - start, 1)

                        header = f"===== EMAIL GENERATOR =====\nRecipient: {recipient}\nPurpose: {purpose}\nTone: {email_tone}\n\n"
                        full_output = header + email_text

                        st.session_state.email_history.append({
                            "recipient": recipient,
                            "purpose": purpose,
                            "tone": email_tone,
                            "output": full_output,
                        })
                        st.session_state.total_generated += 1

                        st.success(f"✓ Generated in {elapsed}s")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "⬇ Download email_output.txt",
                            data=full_output,
                            file_name="email_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"❌ {e}")

        elif st.session_state.email_history:
            last = st.session_state.email_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇ Download email_output.txt",
                data=last["output"],
                file_name="email_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:rgba(0,0,0,0.25);">
                <div style="font-size:2.5rem; margin-bottom:0.6rem;">📧</div>
                <div style="font-size:0.9rem; font-weight:500;">
                    Configure and click <strong style="color:rgba(0,0,0,0.4);">Generate</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — RESUME BUILDER
# ══════════════════════════════════════════════
with tab_resume_builder:
    st.markdown('<div class="section-header">📄 Structured Resume Builder — AI-Powered ATS Resume</div>', unsafe_allow_html=True)

    col_form, col_out = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("**👤 Personal Information**")
        r_name     = st.text_input("Full Name",          placeholder="e.g. Kishanraj B", key="rb_name")
        r_title    = st.text_input("Target Job Title",   placeholder="e.g. Data Scientist / AI Engineer", key="rb_title")
        r_email    = st.text_input("Email",              placeholder="you@email.com", key="rb_email")
        r_phone    = st.text_input("Phone",              placeholder="+91 98765 43210", key="rb_phone")
        r_location = st.text_input("Location",           placeholder="Bengaluru, India", key="rb_location")

        st.markdown("---")

        st.markdown("**✍ Professional Summary**")
        r_summary = st.text_area(
            "Brief summary or raw notes",
            placeholder="e.g. 3 years in AI/ML, built LLM web apps, love Python...",
            height=85, key="rb_summary"
        )

        st.markdown("---")

        st.markdown("**💼 Work Experience**")
        r_experience = st.text_area(
            "List roles (company, title, dates, achievements)",
            placeholder=(
                "SmartGen AI | AI Engineer | Jan 2024 – Present\n"
                "• Built full-stack GenAI studio using Gemini APIs\n"
                "• Reduced resume tailoring time by 75%\n\n"
                "TechCorp | Intern | Jun 2023 – Dec 2023\n"
                "• Developed data pipelines in Python and FastAPI"
            ),
            height=150, key="rb_experience"
        )

        st.markdown("---")

        st.markdown("**🎓 Education**")
        r_education = st.text_area(
            "Degree, Institution, Year",
            placeholder="B.E. in Computer Science | VTU | 2024 | CGPA: 8.8",
            height=70, key="rb_education"
        )

        st.markdown("---")

        st.markdown("**⚡ Skills**")
        r_skills = st.text_area(
            "Skills list",
            placeholder="Python, Streamlit, Google Gemini API, Docker, React, Machine Learning, Git",
            height=70, key="rb_skills"
        )

        st.markdown("---")

        with st.expander("➕ Projects & Certifications (optional)"):
            r_projects = st.text_area(
                "Projects (name, description, tech stack)",
                placeholder="SmartGen AI | End-to-end Career & Content Platform | Python, Streamlit, Gemini",
                height=90, key="rb_projects"
            )
            r_certifications = st.text_area(
                "Certifications",
                placeholder="Google GenAI Professional | 2024",
                height=65, key="rb_certs"
            )

        st.markdown(f"""
        <div class="metric-row" style="margin-top:0.5rem;">
            <span class="metric-chip">🌡 Temp: 0.2</span>
            <span class="metric-chip">📋 ATS-optimised</span>
            <span class="metric-chip">✦ Action verbs</span>
        </div>
        """, unsafe_allow_html=True)

        build_resume_btn = st.button("✦ Build Structured Resume", use_container_width=True, key="rb_build_btn")

    with col_out:
        st.markdown('<div class="section-header">📄 Generated Resume</div>', unsafe_allow_html=True)

        if build_resume_btn:
            if not api_key:
                st.error("❌ Please enter your Gemini API Key in the sidebar.")
            elif not r_name.strip():
                st.warning("⚠️ Please enter your full name.")
            elif not r_title.strip():
                st.warning("⚠️ Please enter your target job title.")
            elif not r_experience.strip():
                st.warning("⚠️ Please add work experience.")
            elif not r_skills.strip():
                st.warning("⚠️ Please list your skills.")
            else:
                with st.spinner("Building your resume…"):
                    try:
                        start = time.time()
                        resume_text = generate_resume(
                            name=r_name, job_title=r_title,
                            email=r_email, phone=r_phone, location=r_location,
                            summary=r_summary or "Generate a strong summary.",
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

                        st.success(f"✓ Resume built in {elapsed}s")
                        st.markdown(f'<div class="output-box">{resume_text}</div>', unsafe_allow_html=True)
                        st.download_button(
                            f"⬇ Download {file_name}",
                            data=resume_text,
                            file_name=file_name,
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"❌ {e}")

        elif st.session_state.resume_history:
            last = st.session_state.resume_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                f"⬇ Download {last['file']}",
                data=last["output"],
                file_name=last["file"],
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3.5rem 2rem; color:rgba(0,0,0,0.25);">
                <div style="font-size:2.5rem; margin-bottom:0.6rem;">📄</div>
                <div style="font-size:0.9rem; font-weight:500;">
                    Fill the form and click <strong style="color:rgba(0,0,0,0.4);">Build Structured Resume</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — HISTORY & ANALYTICS
# ══════════════════════════════════════════════
with tab_history:
    col_b, col_e = st.columns(2, gap="large")

    with col_b:
        st.markdown('<div class="section-header">📝 Blog History</div>', unsafe_allow_html=True)
        if st.session_state.blog_history:
            for i, item in enumerate(reversed(st.session_state.blog_history), 1):
                with st.expander(f"#{len(st.session_state.blog_history)+1-i} — {item['topic'][:45]}"):
                    st.markdown(f"""
                    <div class="metric-row">
                        <span class="metric-chip">🎨 {item['tone']}</span>
                        <span class="metric-chip">📏 {item['word_count']} words</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text(item["output"])
                    st.download_button("⬇ Download", data=item["output"],
                                       file_name=f"blog_{i}.txt", mime="text/plain",
                                       key=f"dl_blog_{i}")
        else:
            st.info("No blogs generated yet.")

    with col_e:
        st.markdown('<div class="section-header">📧 Email History</div>', unsafe_allow_html=True)
        if st.session_state.email_history:
            for i, item in enumerate(reversed(st.session_state.email_history), 1):
                with st.expander(f"#{len(st.session_state.email_history)+1-i} — To: {item['recipient'][:35]}"):
                    st.markdown(f"""
                    <div class="metric-row">
                        <span class="metric-chip">🎯 {item['purpose'][:25]}</span>
                        <span class="metric-chip">✍ {item['tone']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text(item["output"])
                    st.download_button("⬇ Download", data=item["output"],
                                       file_name=f"email_{i}.txt", mime="text/plain",
                                       key=f"dl_email_{i}")
        else:
            st.info("No emails generated yet.")

    if st.session_state.resume_history:
        st.divider()
        st.markdown('<div class="section-header">📄 Resume History</div>', unsafe_allow_html=True)
        for i, item in enumerate(reversed(st.session_state.resume_history), 1):
            with st.expander(f"#{len(st.session_state.resume_history)+1-i} — {item['name']} | {item['title'][:35]}"):
                st.text(item["output"])
                st.download_button("⬇ Download", data=item["output"],
                                   file_name=item["file"], mime="text/plain",
                                   key=f"dl_resume_{i}")

    if st.session_state.blog_history or st.session_state.email_history or st.session_state.resume_history:
        st.divider()
        if st.button("🗑 Clear All History", type="secondary"):
            st.session_state.blog_history  = []
            st.session_state.email_history = []
            st.session_state.resume_history = []
            st.session_state.total_generated = 0
            st.rerun()
