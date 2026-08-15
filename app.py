"""
SmartGen AI — Streamlit App
---------------------------
A premium Streamlit web application that generates blogs and emails
using the Google Gemini API with custom system instructions,
temperatures, and formatted outputs.
"""

import streamlit as st
import os
import time

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartGen AI — Blog & Email Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Premium Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root & Background ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 40%, #0a0a14 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a0a14 100%);
    border-right: 1px solid rgba(139, 92, 246, 0.15);
}

[data-testid="stSidebar"] .stMarkdown h2 {
    color: #a78bfa;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1e1040 0%, #0f0f2e 40%, #1a0f30 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(139,92,246,0.08) 0%, transparent 60%);
    animation: pulse-glow 4s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: rgba(200, 180, 255, 0.7);
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* ── Card Containers ── */
.card {
    background: rgba(15, 15, 35, 0.8);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(20px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    border-color: rgba(139, 92, 246, 0.4);
    box-shadow: 0 0 30px rgba(139, 92, 246, 0.1);
}

/* ── Tab Styling ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(10, 10, 20, 0.8);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(139, 92, 246, 0.15);
}

[data-testid="stTabs"] button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
    color: rgba(180, 160, 255, 0.7);
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #5b21b6);
    color: white;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
}

/* ── Input Fields ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(20, 15, 40, 0.8) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 10px !important;
    color: #e2d9f3 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(139, 92, 246, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
.stSelectbox label,
.stTextInput label,
.stNumberInput label {
    color: #c4b5fd !important;
    font-weight: 500;
    font-size: 0.9rem;
}

/* ── Primary Button ── */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5) !important;
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Output Area ── */
.output-box {
    background: rgba(8, 8, 20, 0.9);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 12px;
    padding: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #d4c5ff;
    line-height: 1.7;
    max-height: 500px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

.output-box::-webkit-scrollbar {
    width: 6px;
}
.output-box::-webkit-scrollbar-track {
    background: rgba(15, 15, 35, 0.5);
    border-radius: 3px;
}
.output-box::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.5);
    border-radius: 3px;
}

/* ── Metric Cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.metric-chip {
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: #c4b5fd;
    font-weight: 500;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: #a78bfa;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(139, 92, 246, 0.15);
}

/* ── Status badges ── */
.badge-success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.badge-ai {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #818cf8;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Sidebar items ── */
.sidebar-stat {
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    color: #c4b5fd;
    font-size: 0.9rem;
}

/* ── Slider ── */
[data-testid="stSlider"] .st-cc,
[data-testid="stSlider"] .st-cd {
    background: rgba(139, 92, 246, 0.3);
}

/* ── Streamlit columns ── */
[data-testid="stHorizontalBlock"] {
    gap: 1.2rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper: Gemini API call (Dual-Layer: SDK + Direct REST API)
# ─────────────────────────────────────────────
def call_gemini(system_instruction: str, prompt: str, temperature: float, api_key: str, model: str = "gemini-2.0-flash") -> str:
    """
    Calls Google Gemini API using:
    1. Official modern google-genai SDK
    2. Direct HTTPS REST API fallback (guaranteed to work across all Python versions/environments)
    With automatic model fallback (gemini-2.0-flash, gemini-1.5-flash, gemini-2.0-flash-lite, gemini-1.5-pro).
    """
    import json
    import requests

    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please enter it in the sidebar.")

    candidate_models = [model, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro"]
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]
    errors = []

    # 1. Try google-genai SDK
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        for m in models_to_try:
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                )
                response = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=config
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as err:
                errors.append(f"SDK ({m}): {err}")
    except Exception as err:
        errors.append(f"SDK Init: {err}")

    # 2. Guaranteed Direct REST API Fallback (Zero dependency on SDK/grpcio)
    for m in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "systemInstruction": {
                    "parts": [
                        {"text": system_instruction}
                    ]
                },
                "generationConfig": {
                    "temperature": temperature
                }
            }

            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
            else:
                try:
                    err_msg = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    err_msg = resp.text
                errors.append(f"REST API ({m} - HTTP {resp.status_code}): {err_msg}")
        except Exception as err:
            errors.append(f"REST API ({m}): {err}")

    raise RuntimeError(
        "Failed to generate content via Gemini API:\n" + "\n".join(errors[-4:])
    )


def generate_blog(topic: str, tone: str, word_count: int, api_key: str, model: str = "gemini-2.0-flash") -> str:
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


def generate_email(recipient: str, purpose: str, tone: str, api_key: str, model: str = "gemini-2.0-flash") -> str:
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


# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "blog_history" not in st.session_state:
    st.session_state.blog_history = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []
if "total_generated" not in st.session_state:
    st.session_state.total_generated = 0


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:2.5rem;">✨</div>
        <div style="font-size:1.2rem; font-weight:800; 
             background: linear-gradient(135deg, #a78bfa, #60a5fa);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">SmartGen AI</div>
        <div style="color:rgba(180,160,255,0.5); font-size:0.75rem; margin-top:0.2rem;">
            Powered by Google Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔑 API Configuration")
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
        placeholder="Enter your Gemini API Key (AIzaSy...)...",
        help="Get your free API key at https://aistudio.google.com/app/apikey",
    )

    model_choice = st.selectbox(
        "Gemini Model",
        options=["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro"],
        index=0,
        help="Model used for content generation. Default is gemini-2.0-flash.",
    )

    if api_key:
        st.markdown('<div class="badge-success">✓ API Key configured</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Enter your API Key to generate content.")

    st.divider()
    st.markdown("### 📊 Session Stats")
    st.markdown(f"""
    <div class="sidebar-stat">📝 Blogs Generated: <strong>{len(st.session_state.blog_history)}</strong></div>
    <div class="sidebar-stat">📧 Emails Generated: <strong>{len(st.session_state.email_history)}</strong></div>
    <div class="sidebar-stat">🎯 Total Outputs: <strong>{st.session_state.total_generated}</strong></div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("""
    <div style="color:rgba(180,160,255,0.6); font-size:0.82rem; line-height:1.6;">
    SmartGen AI uses Google's Gemini models to create premium content.<br><br>
    🌡️ <strong style="color:#c4b5fd;">Blog temp:</strong> 0.7 (creative)<br>
    🌡️ <strong style="color:#c4b5fd;">Email temp:</strong> 0.3 (precise)<br><br>
    <a href="https://aistudio.google.com/app/apikey" target="_blank" 
       style="color:#a78bfa; text-decoration:none;">
       🔗 Get your free API key
    </a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✨ SmartGen AI</div>
    <div class="hero-subtitle">
        Generate stunning blogs & professional emails powered by Google Gemini — 
        your intelligent content co-pilot.
    </div>
    <div style="margin-top:1rem; display:flex; gap:0.6rem; flex-wrap:wrap;">
        <span class="metric-chip">🤖 Gemini 2.0 Flash</span>
        <span class="metric-chip">📝 Blog Generator</span>
        <span class="metric-chip">📧 Email Writer</span>
        <span class="metric-chip">⚡ Real-time Generation</span>
        <span class="metric-chip">💾 Download Outputs</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Main Tabs
# ─────────────────────────────────────────────
tab_blog, tab_email, tab_history = st.tabs(["📝  Blog Generator", "📧  Email Writer", "📚  History"])


# ══════════════════════════════════════════════
# TAB 1 — BLOG GENERATOR
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
            <span class="metric-chip">🌡️ Temperature: 0.7</span>
            <span class="metric-chip">📏 ~{word_count} words</span>
            <span class="metric-chip">🎨 {tone} tone</span>
        </div>
        """, unsafe_allow_html=True)

        generate_blog_btn = st.button("✨ Generate Blog Post", use_container_width=True, key="gen_blog")

    with col_right:
        st.markdown('<div class="section-header">📄 Generated Blog</div>', unsafe_allow_html=True)

        if generate_blog_btn:
            if not api_key:
                st.error("❌ Please enter your Gemini API Key in the sidebar.")
            elif not topic.strip():
                st.warning("⚠️ Please enter a blog topic.")
            else:
                with st.spinner("🤖 Gemini is crafting your blog post..."):
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

                        st.success(f"✅ Generated in {elapsed}s")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)

                        # Download button
                        st.download_button(
                            "⬇️ Download blog_output.txt",
                            data=full_output,
                            file_name="blog_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        elif st.session_state.blog_history:
            last = st.session_state.blog_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download blog_output.txt",
                data=last["output"],
                file_name="blog_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem; color:rgba(180,160,255,0.35);">
                <div style="font-size:3rem;">📝</div>
                <div style="margin-top:0.5rem; font-size:0.95rem;">
                    Configure your blog and click <strong>Generate</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — EMAIL WRITER
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
                "Custom...",
            ],
            index=0,
        )

        if purpose == "Custom...":
            purpose = st.text_input("Describe the email purpose:", placeholder="e.g. Requesting project extension")

        email_tone = st.selectbox(
            "Email Tone",
            options=["professional", "formal", "friendly", "casual", "assertive"],
            index=0,
        )

        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-chip">🌡️ Temperature: 0.3</span>
            <span class="metric-chip">✍️ {email_tone} tone</span>
        </div>
        """, unsafe_allow_html=True)

        generate_email_btn = st.button("✨ Generate Email", use_container_width=True, key="gen_email")

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
                with st.spinner("🤖 Gemini is composing your email..."):
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

                        st.success(f"✅ Generated in {elapsed}s")
                        st.markdown(f'<div class="output-box">{full_output}</div>', unsafe_allow_html=True)

                        st.download_button(
                            "⬇️ Download email_output.txt",
                            data=full_output,
                            file_name="email_output.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        elif st.session_state.email_history:
            last = st.session_state.email_history[-1]
            st.markdown(f'<div class="output-box">{last["output"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download email_output.txt",
                data=last["output"],
                file_name="email_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem; color:rgba(180,160,255,0.35);">
                <div style="font-size:3rem;">📧</div>
                <div style="margin-top:0.5rem; font-size:0.95rem;">
                    Configure your email and click <strong>Generate</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — HISTORY
# ══════════════════════════════════════════════
with tab_history:
    col_b, col_e = st.columns(2, gap="large")

    with col_b:
        st.markdown('<div class="section-header">📝 Blog History</div>', unsafe_allow_html=True)
        if st.session_state.blog_history:
            for i, item in enumerate(reversed(st.session_state.blog_history), 1):
                with st.expander(f"#{len(st.session_state.blog_history)+1-i} — {item['topic'][:40]}..."):
                    st.markdown(f"""
                    <div class="metric-row">
                        <span class="metric-chip">🎨 {item['tone']}</span>
                        <span class="metric-chip">📏 {item['word_count']} words</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text(item["output"])
                    st.download_button(
                        f"⬇️ Download",
                        data=item["output"],
                        file_name=f"blog_{i}.txt",
                        mime="text/plain",
                        key=f"dl_blog_{i}"
                    )
        else:
            st.info("No blogs generated yet. Head to the Blog Generator tab!")

    with col_e:
        st.markdown('<div class="section-header">📧 Email History</div>', unsafe_allow_html=True)
        if st.session_state.email_history:
            for i, item in enumerate(reversed(st.session_state.email_history), 1):
                with st.expander(f"#{len(st.session_state.email_history)+1-i} — To: {item['recipient'][:35]}"):
                    st.markdown(f"""
                    <div class="metric-row">
                        <span class="metric-chip">🎯 {item['purpose'][:25]}</span>
                        <span class="metric-chip">✍️ {item['tone']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text(item["output"])
                    st.download_button(
                        f"⬇️ Download",
                        data=item["output"],
                        file_name=f"email_{i}.txt",
                        mime="text/plain",
                        key=f"dl_email_{i}"
                    )
        else:
            st.info("No emails generated yet. Head to the Email Writer tab!")

    if st.session_state.blog_history or st.session_state.email_history:
        st.divider()
        if st.button("🗑️ Clear All History", type="secondary"):
            st.session_state.blog_history = []
            st.session_state.email_history = []
            st.session_state.total_generated = 0
            st.rerun()
