import os
import google.generativeai as genai


def summarize_quality_issues(
    source_text: str, translated_text: str, target_language: str
) -> str:
    """
    Uses a generative model to identify and summarize quality issues in a translation.

    Args:
        source_text: The original source text.
        translated_text: The translated text.
        target_language: The language of the translation.

    Returns:
        A summary of potential quality issues.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Please review the following translation for quality.
    Source Text: "{source_text}"
    Translated Text ({target_language}): "{translated_text}"
    
    Identify any potential issues such as mistranslations, grammatical errors, awkward phrasing, or loss of nuance.
    Provide a brief summary of the translation quality.
    """

    response = model.generate_content(prompt)
    return response.text
