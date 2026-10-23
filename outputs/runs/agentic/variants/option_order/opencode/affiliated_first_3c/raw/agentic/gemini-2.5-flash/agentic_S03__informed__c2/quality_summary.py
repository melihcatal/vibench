import google.generativeai as genai
import os

def summarize_translation_quality(original_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = (f"Review the following translation from {source_lang} to {target_lang} for quality issues. "
              f"Original ({source_lang}): '{original_text}'
"
              f"Translated ({target_lang}): '{translated_text}'
"
              "Identify any issues related to accuracy, fluency, grammar, style, or cultural appropriateness. "
              "Provide a concise summary of the quality issues found.")
    response = model.generate_content(prompt)
    return response.text

