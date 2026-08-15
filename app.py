"""
SmartGen AI — Streamlit App
---------------------------
Minimalistic glassmorphism UI — white background, black text, frosted glass cards.
Powered by Google Gemini REST API (gemini-3.5-flash).
"""

import streamlit as st
import os
import time

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartGen AI — Blog & Email Generator",
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

/* ── Background — clean white with very subtle grain ── */
.stApp {
    background: #f5f5f7;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(180,200,255,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(200,220,255,0.12) 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.7);
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
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 24px;
    padding: 2.8rem 3.2rem;
    margin-bottom: 2rem;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.06),
        0 1px 0 rgba(255,255,255,0.9) inset;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(60,60,60,0.12), transparent);
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #0a0a0a;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.15;
}

.hero-title span {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: rgba(10, 10, 10, 0.55);
    font-size: 1.05rem;
    margin-top: 0.6rem;
    font-weight: 400;
    letter-spacing: -0.01em;
}

/* ── Glass Cards ── */
.glass-card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 2rem;
    box-shadow:
        0 4px 24px rgba(0, 0, 0, 0.05),
        0 1px 0 rgba(255,255,255,0.95) inset;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.glass-card:hover {
    box-shadow:
        0 8px 40px rgba(0, 0, 0, 0.09),
        0 1px 0 rgba(255,255,255,0.95) inset;
    transform: translateY(-1px);
}

/* ── Tab Styling ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(16px);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid rgba(0,0,0,0.07);
    gap: 4px;
}

[data-testid="stTabs"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: rgba(0,0,0,0.45) !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.2rem !important;
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
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 12px !important;
    color: #0a0a0a !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,0,0,0.3) !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06) !important;
}

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stTextInput label p,
.stNumberInput label p,
.stSlider label p {
    color: #111111 !important;
    font-weight: 500 !important;
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
    padding: 0.65rem 2rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18) !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.01em !important;
}

.stButton > button:hover {
    background: #1a1a1a !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,0,0,0.25) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}

/* ── Download button — outlined ── */
[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.8) !important;
    color: #0a0a0a !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,255,255,1) !important;
    border-color: rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Output Area ── */
.output-box {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.84rem;
    color: #1a1a1a;
    line-height: 1.75;
    max-height: 500px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.output-box::-webkit-scrollbar { width: 5px; }
.output-box::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.03);
    border-radius: 3px;
}
.output-box::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.15);
    border-radius: 3px;
}

/* ── Chips / Tags ── */
.metric-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 1.4rem;
}

.metric-chip {
    background: rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 20px;
    padding: 0.28rem 0.85rem;
    font-size: 0.78rem;
    color: #333;
    font-weight: 500;
    letter-spacing: -0.01em;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.05rem;
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

/* ── Badges ── */
.badge-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    color: #15803d;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

/* ── Sidebar stat boxes ── */
.sidebar-stat {
    background: rgba(0,0,0,0.04);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.4rem;
    color: #111;
    font-size: 0.88rem;
    font-weight: 500;
}

/* ── Divider ── */
hr { border-color: rgba(0,0,0,0.07) !important; }

/* ── Slider track ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(0,0,0,0.12) !important;
}

/* ── Alert / Info boxes ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    background: rgba(255,255,255,0.7) !important;
    color: #111 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.55) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    border-radius: 14px !important;
}

/* ── Streamlit columns gap ── */
[data-testid="stHorizontalBlock"] { gap: 1.4rem; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper: Gemini API call (Pure REST API — zero binary dependencies)
# ─────────────────────────────────────────────
def call_gemini(system_instruction: str, prompt: str, temperature: float, api_key: str, model: str = "gemini-3.5-flash") -> str:
    """
    Calls Google Gemini API using the DIRECT REST API only.
    - No google-genai SDK dependency (no grpcio, no protobuf, no AFC warnings)
    - Only requires 'requests' which always installs cleanly on Streamlit Cloud
    - Automatically falls back across multiple models if one fails
    Models tried: gemini-3.5-flash → gemini-3.1-flash-lite → gemini-flash-latest → gemini-3.7-flash
    """
    import json
    import requests

    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please enter it in the sidebar.")

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
    <div style="text-align:center; padding:1.2rem 0 1.8rem;">
        <div style="font-size:2rem; margin-bottom:0.4rem;">✦</div>
        <div style="font-size:1.25rem; font-weight:800; color:#0a0a0a; letter-spacing:-0.03em;">SmartGen AI</div>
        <div style="color:rgba(0,0,0,0.4); font-size:0.75rem; margin-top:0.25rem; font-weight:500;">
            Powered by Google Gemini
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
        "Model",
        options=["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.7-flash"],
        index=0,
        help="Default: gemini-3.5-flash (fastest & most capable for new keys)",
    )

    if api_key:
        st.markdown('<div class="badge-success">✓ API Key ready</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Enter your API Key to start generating.")

    st.divider()

    st.markdown("**📊 Session Stats**")
    st.markdown(f"""
    <div class="sidebar-stat">📝 Blogs &nbsp;&nbsp; <strong>{len(st.session_state.blog_history)}</strong></div>
    <div class="sidebar-stat">📧 Emails &nbsp;&nbsp; <strong>{len(st.session_state.email_history)}</strong></div>
    <div class="sidebar-stat">🎯 Total &nbsp;&nbsp;&nbsp; <strong>{st.session_state.total_generated}</strong></div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="color:rgba(0,0,0,0.45); font-size:0.8rem; line-height:1.7;">
    SmartGen AI uses Google Gemini to create content.<br><br>
    🌡 <strong style="color:#111;">Blog temp:</strong> 0.7 — creative<br>
    🌡 <strong style="color:#111;">Email temp:</strong> 0.3 — precise<br><br>
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
        Generate blogs &amp; professional emails with Google Gemini —
        your minimalist content co-pilot.
    </div>
    <div style="margin-top:1.2rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
        <span class="metric-chip">🤖 Gemini 3.5 Flash</span>
        <span class="metric-chip">📝 Blog Generator</span>
        <span class="metric-chip">📧 Email Writer</span>
        <span class="metric-chip">⚡ Real-time</span>
        <span class="metric-chip">💾 Download</span>
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
# TAB 3 — HISTORY
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
                    st.download_button(
                        "⬇ Download",
                        data=item["output"],
                        file_name=f"blog_{i}.txt",
                        mime="text/plain",
                        key=f"dl_blog_{i}"
                    )
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
                    st.download_button(
                        "⬇ Download",
                        data=item["output"],
                        file_name=f"email_{i}.txt",
                        mime="text/plain",
                        key=f"dl_email_{i}"
                    )
        else:
            st.info("No emails generated yet.")

    if st.session_state.blog_history or st.session_state.email_history:
        st.divider()
        if st.button("🗑 Clear All History", type="secondary"):
            st.session_state.blog_history = []
            st.session_state.email_history = []
            st.session_state.total_generated = 0
            st.rerun()
