import google.generativeai as genai
import os

def summarize_translation_quality(original_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """Summarizes translation quality issues using the Google Gemini API.

    Args:
        original_text: The original text.
        translated_text: The translated text.
        source_lang: The source language code (e.g., 'en').
        target_lang: The target language code (e.g., 'es').

    Returns:
        A summary of potential quality issues or observations.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Analyze the quality of the following translation from {source_lang} to {target_lang}. 
    Identify any potential issues like mistranslations, grammatical errors, unnatural phrasing, or loss of nuance.

    Original ({source_lang}):
    '''{original_text}'''

    Translated ({target_lang}):
    '''{translated_text}'''

    Provide a concise summary of the quality issues or observations.
    """
    
    response = model.generate_content(prompt)
    return response.text
