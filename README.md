# ✦ SmartGen AI — Career Intelligence & Content Studio

A modern **Streamlit web application** and Python toolkit powered by the **Google Gemini REST API** (`gemini-3.5-flash`), featuring an end-to-end **AI Career & Resume Intelligence Pipeline**, **Blog & Email Generation Studio**, and an automated **24/7 Keep-Alive Ping Monitor**.

---

## 🌐 Live App

> **[➡️ Launch SmartGen AI on Streamlit Cloud](https://aenexzgenaimainminiprojectkishanraj-aemnvkurpgtpg7nua7n8n2.streamlit.app/)**

---

## 🚀 4-Step AI Career & Resume Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. Resume Parser │ ──► │ 2. Job Matching  │ ──► │ 3. CV Suggestion │ ──► │ 4. Career Mentor │
│ PDF/DOCX/Text AI │     │ Semantic Scoring │     │ XYZ Bullet Rewr. │     │ Grounded RAG Bot │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

1. **📤 Step 1: Resume Parser**
   - Upload PDF (`.pdf`), Word Document (`.docx`), or plain text (`.txt`).
   - Automatically extracts candidate profile, categorized skills, work history, and computes an **ATS Readiness Score (0–100%)**.

2. **🔍 Step 2: Job Matching & Skill Gap Analysis**
   - Evaluates profile against a curated job corpus or custom pasted Job Descriptions.
   - Computes semantic match %, identifies **✅ Matched Skills** vs **⚠️ Missing Skills to Target**.

3. **✍️ Step 3: CV Suggestions & Bullet Rewriter**
   - Injects high-impact missing keywords into resume context.
   - Rewrites passive bullet points into Google's **XYZ Formula** (*"Accomplished [X] as measured by [Y], by doing [Z]"*).
   - Generates targeted executive summary and full tailored CV.

4. **💬 Step 4: AI Career Mentor (RAG Chatbot)**
   - Grounded chatbot informed by the candidate's resume and target job.
   - 1-Click quick actions: **Mock Interview Questions (STAR method)**, **60-Day Upskilling Roadmap**, **Targeted Cover Letter**, and **Salary Negotiation Scripts**.

---

## 🎨 Minimalistic Glassmorphism UI

- **Canvas**: Clean light background (`#f5f5f7`) with ambient gradient accents.
- **Typography**: High-contrast, crystal-clear `#0a0a0a` text with `Inter` and `JetBrains Mono`.
- **Frosted Glass Cards**: `backdrop-filter: blur(24px)` with subtle shadows and border highlights.
- **Interactive Controls**: Responsive tabs, score badges, chip tags, and smooth action buttons.

---

## 🏓 Ping Monitor — Keep Alive System

SmartGen AI includes a **dual-layer ping monitor** to prevent the Streamlit Cloud app from going to sleep due to inactivity.

### How It Works

```
Every 30 minutes
      │
      ▼
┌─────────────────────────────────────────────┐
│          GitHub Actions (Cloud)             │
│  .github/workflows/keep_alive.yml           │
│                                             │
│  1. Pings APP_URL (main page)               │
│  2. Pings APP_URL/_stcore/health            │
│  3. Logs HTTP status + timestamp            │
│  4. Repeats every 30 min, 24/7 free         │
└─────────────────────────────────────────────┘
      │
      ▼  (optional, local extra layer)
┌─────────────────────────────────────────────┐
│       ping_monitor.py (Local Script)        │
│                                             │
│  - Continuous loop, configurable interval   │
│  - Rich console output + log file           │
│  - Uptime % stats every 10 pings            │
│  - Run: python ping_monitor.py              │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **Frontend / Web Framework**: [Streamlit](https://streamlit.io/)
- **AI Core**: [Google Gemini REST API](https://ai.google.dev/) (`gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemini-flash-latest`)
- **Document Extractors**: `pypdf`, `python-docx`
- **Network / HTTP Client**: `requests`
- **Design System**: Vanilla CSS Glassmorphism + Google Fonts (Inter, JetBrains Mono)
