import google.generativeai as genai
import os

def summarize_translation_quality(original_text: str, translated_text: str, target_language: str) -> str:
    """
    Summarizes potential quality issues in a translated text using Google Gemini API.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Analyze the translation quality between the original text and the translated text into {target_language}. Highlight any potential errors, awkward phrasing, or areas that could be improved. Provide a concise summary of the quality issues.

Original Text: """{original_text}"""
Translated Text: """{translated_text}"""
Summary of Quality Issues:"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set in environment variables)
    original = "The quick brown fox jumps over the lazy dog."
    translated = "Der schnelle braune Fuchs springt über den faulen Hund."
    target_lang = "German"
    summary = summarize_translation_quality(original, translated, target_lang)
    print(f"Original: {original}")
    print(f"Translated: {translated}")
    print(f"Quality Summary: {summary}")
