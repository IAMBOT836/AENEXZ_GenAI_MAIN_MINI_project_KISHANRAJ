"""
Gemini Blog & Email Generator
------------------------------
A Python application for Google Colab and local Python environments that generates
blogs and emails using the Google Gemini API with custom system instructions,
temperatures, and formatted file exports.

Requirements Met:
- generate_blog(topic, tone, word_count) function with system instruction & temp=0.7
- generate_email(recipient, purpose, tone) function with system instruction & temp=0.3
- main() interactive menu
- API Key loaded from Colab Secrets (userdata.get('GEMINI_API_KEY')) or Environment Variable
- Output saved to blog_output.txt and email_output.txt
- Exact sample output format implemented
"""

import os
import sys
import getpass

def get_api_key() -> str:
    """
    Retrieves the Gemini API key from Colab Secrets, environment variables,
    or interactive prompt as fallback.
    """
    # 1. Try Google Colab Secrets (Standard pattern in Colab)
    try:
        import importlib
        colab_userdata = importlib.import_module("google.colab.userdata")
        key = colab_userdata.get('GEMINI_API_KEY') or colab_userdata.get('GOOGLE_API_KEY')
        if key:
            return key
    except Exception:
        pass

    # 2. Try Environment Variables
    key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if key:
        return key

    # 3. Interactive fallback
    print("⚠️ API Key not found in Colab Secrets or Environment Variables.")
    key = getpass.getpass("Please enter your Gemini API Key: ").strip()
    return key


def call_gemini(system_instruction: str, prompt: str, temperature: float, model: str = "gemini-2.0-flash") -> str:
    """
    Calls Google Gemini API using official SDK or direct REST API with automatic model fallback.
    """
    import json
    import requests

    api_key = get_api_key()
    api_key = api_key.strip() if api_key else ""
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required to generate content.")

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
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
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

    # 2. Guaranteed REST API Fallback
    for m in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "systemInstruction": {"parts": [{"text": system_instruction}]},
                "generationConfig": {"temperature": temperature}
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


def generate_blog(topic: str, tone: str, word_count: int, save_file: str = "blog_output.txt") -> str:
    """
    Generates a blog post using Gemini API with temperature 0.7.

    BLOG GENERATOR FEATURES:
    - User inputs: topic, tone (formal / casual / Gen Z / professional), word count
    - System instruction: "You are an experienced blog writer..."
    - Output includes: title, intro hook, 2-3 body sections, conclusion
    - Saves output to text file (e.g. blog_output.txt)
    """
    system_instruction = "You are an experienced blog writer who crafts engaging, insightful, and well-structured articles."

    prompt = f"""
Write a blog post based on the following details:
- Topic: "{topic}"
- Tone: {tone}
- Target Word Count: {word_count} words

Formatting & Structure Guidelines:
1. Title: Create an engaging, catchy title.
2. Intro Hook: Start with a strong hook that captures reader interest.
3. Body Sections: Write 2 to 3 distinct body sections with descriptive subheadings.
4. Conclusion: Summarize main points with a memorable takeaways or call to action.
    """

    blog_text = call_gemini(system_instruction=system_instruction, prompt=prompt, temperature=0.7)

    header = f"===== BLOG GENERATOR =====\nTopic: \"{topic}\"\nTone: {tone}\nWord count: {word_count}\n\n"
    full_output = header + blog_text

    if save_file:
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"💾 Saved blog output to {save_file}")

    return full_output


def generate_email(recipient: str, purpose: str, tone: str, save_file: str = "email_output.txt") -> str:
    """
    Generates a professional email using Gemini API with temperature 0.3.

    EMAIL GENERATOR FEATURES:
    - User inputs: recipient (name/role), purpose (cold outreach / follow-up / thank-you / leave request), tone
    - System instruction: "You are a professional email writer..."
    - Output includes: subject line + body + closing
    - Saves output to text file (e.g. email_output.txt)
    """
    system_instruction = "You are a professional email writer who produces clear, polished, and effective emails."

    prompt = f"""
Write an email based on the following details:
- Recipient: {recipient}
- Purpose: {purpose}
- Tone: {tone}

Formatting & Structure Guidelines:
1. Subject Line: Clear and professional subject line.
2. Salutation: Appropriate greeting to {recipient}.
3. Email Body: Concise, context-appropriate message addressing the purpose ({purpose}).
4. Closing: Professional sign-off with placeholders for sender details.
    """

    email_text = call_gemini(system_instruction=system_instruction, prompt=prompt, temperature=0.3)

    header = f"===== EMAIL GENERATOR =====\nRecipient: {recipient}\nPurpose: {purpose}\nTone: {tone}\n\n"
    full_output = header + email_text

    if save_file:
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"💾 Saved email output to {save_file}")

    return full_output


def main():
    """
    Interactive main menu to tie together blog and email generators.
    """
    print("\n==============================================")
    print("      GEMINI BLOG & EMAIL GENERATOR")
    print("==============================================")

    while True:
        print("\nMENU:")
        print("1. Generate Blog Post")
        print("2. Generate Email")
        print("3. Run Demo (Generate both Blog & Email)")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            print("\n--- BLOG GENERATOR ---")
            topic = input("Enter Topic (default: 'Why Python is the best first language'): ").strip()
            if not topic:
                topic = "Why Python is the best first language"

            tone = input("Enter Tone (formal / casual / Gen Z / professional) [default: casual]: ").strip()
            if not tone:
                tone = "casual"

            wc_input = input("Enter Target Word Count [default: 300]: ").strip()
            try:
                word_count = int(wc_input) if wc_input else 300
            except ValueError:
                word_count = 300

            print("\n⏳ Generating blog post with temperature=0.7...")
            output = generate_blog(topic=topic, tone=tone, word_count=word_count)
            print("\n" + output)

        elif choice == "2":
            print("\n--- EMAIL GENERATOR ---")
            recipient = input("Enter Recipient (default: 'HR Manager, TCS'): ").strip()
            if not recipient:
                recipient = "HR Manager, TCS"

            purpose = input("Enter Purpose (cold outreach / follow-up / thank-you / leave request) [default: 'Follow-up after interview']: ").strip()
            if not purpose:
                purpose = "Follow-up after interview"

            tone = input("Enter Tone (formal / casual / professional) [default: professional]: ").strip()
            if not tone:
                tone = "professional"

            print("\n⏳ Generating email with temperature=0.3...")
            output = generate_email(recipient=recipient, purpose=purpose, tone=tone)
            print("\n" + output)

        elif choice == "3":
            print("\n--- RUNNING DEMO ---")
            print("\n1/2 Generating Blog Post...")
            blog_out = generate_blog(
                topic="Why Python is the best first language",
                tone="casual",
                word_count=300
            )
            print("\n" + blog_out)

            print("\n" + "-"*40 + "\n")

            print("2/2 Generating Email...")
            email_out = generate_email(
                recipient="HR Manager, TCS",
                purpose="Follow-up after interview",
                tone="professional"
            )
            print("\n" + email_out)

        elif choice == "4":
            print("Exiting Gemini Generator. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
