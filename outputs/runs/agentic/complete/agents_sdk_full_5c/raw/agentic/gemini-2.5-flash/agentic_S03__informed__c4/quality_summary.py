import google.generativeai as genai
import os

def summarize_translation_quality(original_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """Summarizes translation quality issues using Gemini API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summarization

    prompt = f"""Review the following translation from {source_lang} to {target_lang} and provide a brief summary of any potential quality issues (e.g., accuracy, fluency, style, tone, grammatical errors, mistranslations). If the translation is good, state that.

Original ({source_lang}): {original_text}
Translated ({target_lang}): {translated_text}

Summary of quality issues:"""

    response = model.generate_content(prompt)
    return response.text
