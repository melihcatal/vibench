import google.generativeai as genai
import os

def summarize_translation_quality(
    translated_text: str,
    original_text: str,
    source_language: str,
    target_language: str,
) -> str:
    """Summarizes potential translation quality issues using Google Gemini API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Review the following translation from {source_language} to {target_language} for quality issues.
Original Text ({source_language}):
'''{original_text}'''

Translated Text ({target_language}):
'''{translated_text}'''

Identify any potential issues related to accuracy, fluency, grammar, style, or cultural appropriateness. Provide a concise summary of the findings.
"""
    response = model.generate_content(prompt)
    return response.text
