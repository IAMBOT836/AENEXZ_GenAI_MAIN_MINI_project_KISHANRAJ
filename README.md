# Gemini Blog & Email Generator

A complete Python application built for Google Colab and local Python environments that generates custom blog posts and professional emails using the **Google Gemini API**.

---

## 🎯 Goal
Build a Python application (in Google Colab) that generates blogs and emails using the Gemini API, following clean architectural patterns with system instructions, customizable parameters, temperature control, and formatted file exports.

---

## ✅ Feature Verification Checklist

| Requirement | Implementation Status | Location |
| :--- | :---: | :--- |
| **`generate_blog(topic, tone, word_count)`** | ✅ Implemented | `main.py`, `gemini_content_generator.ipynb` |
| **`generate_email(recipient, purpose, tone)`** | ✅ Implemented | `main.py`, `gemini_content_generator.ipynb` |
| **`main()` Interactive Menu** | ✅ Implemented | `main.py`, `gemini_content_generator.ipynb` |
| **API Key loaded from Colab Secrets** | ✅ Implemented (`userdata.get('GEMINI_API_KEY')`) | `main.py`, `gemini_content_generator.ipynb` |
| **Temperature 0.7 for Blog** | ✅ Implemented | `generate_blog()` |
| **Temperature 0.3 for Email** | ✅ Implemented | `generate_email()` |
| **Save outputs to text files** | ✅ Implemented (`blog_output.txt`, `email_output.txt`) | File system output |
| **System Instruction: Blog** | `"You are an experienced blog writer..."` | `generate_blog()` |
| **System Instruction: Email** | `"You are a professional email writer..."` | `generate_email()` |
| **Exact Output Formatting** | Matches sample submission headers (`===== BLOG GENERATOR =====`, etc.) | Output formatters |

---

## 📂 Repository Structure

```text
SmartgenAi/
├── main.py                       # Main executable Python application
├── gemini_content_generator.ipynb # Jupyter Notebook for Google Colab
├── blog_output.txt                # Sample generated blog output file
├── email_output.txt               # Sample generated email output file
└── README.md                      # Documentation & instructions
```

---

## 🚀 How to Run in Google Colab

1. **Upload Notebook**:
   - Open [Google Colab](https://colab.research.google.com/).
   - Click **File > Upload Notebook** and select [`gemini_content_generator.ipynb`](file:///c:/Users/Kishanraj/SmartgenAi/gemini_content_generator.ipynb).

2. **Add Gemini API Key to Colab Secrets**:
   - Click the 🗝️ **Secrets** icon on the left sidebar in Colab.
   - Click **+ Add new secret**.
   - Set **Name**: `GEMINI_API_KEY`
   - Set **Value**: *Your Gemini API Key*
   - Toggle **Notebook access** ON.

3. **Run Cells**:
   - Run Step 1 (Install Dependencies).
   - Run Step 2 (Setup API & Functions).
   - Run Step 5 (`main()`) to launch the interactive generator menu!

---

## 🖥️ How to Run Locally

1. **Install Dependencies**:
   ```bash
   pip install google-genai
   ```

2. **Set Environment Variable (Optional)**:
   - Windows PowerShell:
     ```powershell
     $env:GEMINI_API_KEY="your-api-key-here"
     ```
   - Mac/Linux:
     ```bash
     export GEMINI_API_KEY="your-api-key-here"
     ```

3. **Run Application**:
   ```bash
   python main.py
   ```

---

## 📄 Output File Examples

### `blog_output.txt`
```text
===== BLOG GENERATOR =====
Topic: "Why Python is the best first language"
Tone: casual
Word count: 300

Title: Why Python Should Be Your First Programming Language

Intro:
Thinking about diving into the world of coding...
[Full blog body]
```

### `email_output.txt`
```text
===== EMAIL GENERATOR =====
Recipient: HR Manager, TCS
Purpose: Follow-up after interview
Tone: professional

Subject: Following Up: Interview for Software Engineer Position - [Your Name]

Dear HR Manager,
...
[Full email body]
```
