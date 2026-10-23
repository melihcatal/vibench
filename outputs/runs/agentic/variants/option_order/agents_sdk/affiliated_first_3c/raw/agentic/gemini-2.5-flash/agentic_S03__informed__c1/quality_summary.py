import os
import google.generativeai as genai

def summarize_translation_quality_issues(original_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Analyze the following translation from {source_lang} to {target_lang} for any quality issues such as grammatical errors, unnatural phrasing, or inaccuracies. Provide a concise summary of the problems found.

Original ({source_lang}):
{original_text}

Translated ({target_lang}):
{translated_text}

Quality Issues Summary:"""

    response = model.generate_content(prompt)
    return response.text
