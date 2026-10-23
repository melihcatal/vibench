import google.generativeai as genai
import os

def summarize_translation_quality(original_text: str, translated_text: str, issues: str) -> str:
    """Summarizes translation quality issues using Google Gemini API.

    Args:
        original_text: The original text.
        translated_text: The translated text.
        issues: A description of identified quality issues (e.g., "grammar errors, awkward phrasing").

    Returns:
        A summary of the translation quality issues.
    """
    # Configure the Gemini API with an API key from environment variables
    # Ensure GOOGLE_API_KEY is set in your environment.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summarization

    prompt = (
        f"Summarize the translation quality issues for the following text pair:\n"
        f"Original: {original_text}\n"
        f"Translated: {translated_text}\n"
        f"Identified issues: {issues}\n\n"
        f"Provide a concise summary of the quality problems."
    )

    response = model.generate_content(prompt)
    return response.text
