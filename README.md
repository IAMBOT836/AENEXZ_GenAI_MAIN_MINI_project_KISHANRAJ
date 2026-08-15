# ✨ SmartGen AI — Gemini Blog & Email Generator

A premium **Streamlit web application** and Python toolkit that generates custom blog posts and professional emails using the **Google Gemini API** — with a built-in **24/7 Ping Monitor** to keep the app alive on Streamlit Cloud.

---

## 🌐 Live App

> **[➡️ Launch SmartGen AI on Streamlit Cloud](https://your-app.streamlit.app)**
>
> *(Replace this link once deployed via [share.streamlit.io](https://share.streamlit.io))*

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

### 🛠️ Setup the GitHub Actions Ping Monitor

1. **Deploy your app** to [Streamlit Cloud](https://share.streamlit.io) and copy the URL (e.g. `https://myapp.streamlit.app`)

2. **Add a GitHub Secret** in your repo:
   - Go to → **Settings → Secrets and Variables → Actions → New repository secret**
   - Name: `APP_URL`
   - Value: `https://your-app.streamlit.app`

3. **That's it!** GitHub Actions will automatically ping your app every 30 minutes, forever — for free.

4. **Check ping logs** anytime at: `Repo → Actions → 🏓 Ping Monitor — Keep App Alive`

### 🖥️ Run the Local Ping Monitor

For an extra layer of reliability, you can also run the local monitor:

```bash
# Basic usage (uses APP_URL env var or placeholder)
python ping_monitor.py

# With your actual URL
python ping_monitor.py --url https://your-app.streamlit.app

# Custom interval (20 minutes)
python ping_monitor.py --url https://your-app.streamlit.app --interval 20
```

**Output example:**
```
  ╔══════════════════════════════════════════════╗
  ║       SmartGen AI — Ping Monitor 🏓          ║
  ║  Keeping your Streamlit app alive 24/7       ║
  ╚══════════════════════════════════════════════╝

2026-08-15 05:30:00 [INFO] 📡 Ping #1 starting...
2026-08-15 05:30:02 [INFO] ✅ 2026-08-15 00:00:02 UTC — ALIVE  (HTTP 200 | Health: 200)
2026-08-15 05:30:02 [INFO] ⏳ Next ping in 30 minutes...

2026-08-15 06:00:00 [INFO] 📡 Ping #2 starting...
2026-08-15 06:00:03 [INFO] ✅ 2026-08-15 00:30:03 UTC — ALIVE  (HTTP 200 | Health: 200)
```

---

## 🎯 Features

| Feature | Details |
| :--- | :--- |
| 📝 **Blog Generator** | Topic, tone, word count → AI-crafted blog post |
| 📧 **Email Writer** | Recipient, purpose, tone → Professional email |
| 📚 **Session History** | View + download all past generations |
| 🏓 **Ping Monitor** | GitHub Actions cron + local script to prevent sleep |
| 💾 **Download Outputs** | `.txt` file download for every generation |
| 🌡️ **Temperature Control** | 0.7 for blogs (creative), 0.3 for emails (precise) |
| 🔑 **Secure API Key** | Sidebar input or environment variable |

---

## ✅ Requirements Checklist

| Requirement | Status | Location |
| :--- | :---: | :--- |
| `generate_blog(topic, tone, word_count)` | ✅ | `app.py`, `main.py`, `gemini_content_generator.ipynb` |
| `generate_email(recipient, purpose, tone)` | ✅ | `app.py`, `main.py`, `gemini_content_generator.ipynb` |
| `main()` Interactive Menu | ✅ | `main.py`, `gemini_content_generator.ipynb` |
| API Key from Colab Secrets / Env Var | ✅ | `userdata.get('GEMINI_API_KEY')` |
| Temperature 0.7 for Blog | ✅ | `generate_blog()` |
| Temperature 0.3 for Email | ✅ | `generate_email()` |
| Save outputs to `.txt` files | ✅ | `blog_output.txt`, `email_output.txt` |
| System Instructions | ✅ | Both generator functions |
| Streamlit Web App | ✅ | `app.py` |
| **24/7 Ping Monitor** | ✅ | `.github/workflows/keep_alive.yml`, `ping_monitor.py` |

---

## 📂 Repository Structure

```text
SmartgenAi/
├── app.py                              # ✨ Streamlit web app (premium UI)
├── main.py                             # CLI Python app with interactive menu
├── ping_monitor.py                     # 🏓 Local ping monitor script
├── gemini_content_generator.ipynb      # Jupyter Notebook for Google Colab
├── requirements.txt                    # Python dependencies
├── .github/
│   └── workflows/
│       └── keep_alive.yml              # 🤖 GitHub Actions — pings app every 30 min
├── blog_output.txt                     # Sample blog output
├── email_output.txt                    # Sample email output
└── README.md                           # This file
```

---

## 🚀 Quickstart

### Option A — Streamlit Web App (Recommended)

```bash
pip install -r requirements.txt
streamlit run app.py
```
Open **http://localhost:8501** — enter your Gemini API key in the sidebar and generate!

### Option B — CLI (Terminal)

```bash
pip install google-genai
python main.py
```

### Option C — Google Colab

1. Open [`gemini_content_generator.ipynb`](gemini_content_generator.ipynb) in Colab
2. Add `GEMINI_API_KEY` to Colab Secrets (🗝️ icon)
3. Run all cells and use the interactive menu

---

## 🔑 API Key Setup

| Environment | Method |
| :--- | :--- |
| **Streamlit Cloud** | Settings → Secrets → `GEMINI_API_KEY = "your-key"` |
| **Local** | `$env:GEMINI_API_KEY="your-key"` (PowerShell) or set in sidebar |
| **Colab** | Secrets panel → `GEMINI_API_KEY` |
| **Get a key** | [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) (free) |

---

## 📄 Sample Outputs

### `blog_output.txt`
```
===== BLOG GENERATOR =====
Topic: "Why Python is the best first language"
Tone: casual
Word count: 300

Title: Why Python Should Be Your First Programming Language
...
```

### `email_output.txt`
```
===== EMAIL GENERATOR =====
Recipient: HR Manager, TCS
Purpose: Follow-up after interview
Tone: professional

Subject: Following Up: Interview for Software Engineer Position
...
```

---

## 🛠️ Tech Stack

- **[Google Gemini API](https://ai.google.dev/)** — `gemini-2.0-flash` model
- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[GitHub Actions](https://github.com/features/actions)** — Ping monitor automation
- **Python 3.10+**

---

*Built by [Kishanraj](https://github.com/IAMBOT836) · Powered by Google Gemini*
