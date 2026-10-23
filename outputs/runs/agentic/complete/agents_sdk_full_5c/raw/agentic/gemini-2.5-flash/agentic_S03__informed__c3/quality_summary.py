import os
import google.generativeai as genai

def summarize_translation_quality(
    original_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
    api_key: str = None,
) -> str:
    """
    Summarizes potential quality issues between an original text and its translation
    using the Google Gemini API.
    """
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following original text and its translation. Identify any potential quality issues
    such as grammatical errors, unnatural phrasing, mistranslations, omissions, or additions.
    Provide a concise summary of the identified issues.

    Original ({source_language}):
    '''{original_text}'''

    Translation ({target_language}):
    '''{translated_text}'''

    Summary of translation quality issues:
    """

    response = model.generate_content(prompt)
    return response.text
