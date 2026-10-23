import google.generativeai as genai
import os


def summarize_quality_issues(
    translation_text: str, source_text: str, issues: str
) -> str:
    """Summarizes translation quality issues using Google Gemini API.

    Args:
        translation_text: The translated text.
        source_text: The original source text.
        issues: A description of identified quality issues.

    Returns:
        A summary of the translation quality issues.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
Given the original source text, its translation, and identified quality issues, summarize the quality problems concisely.

Source Text: {source_text}
Translation Text: {translation_text}
Quality Issues: {issues}

Summary of Quality Issues:
"""

    response = model.generate_content(prompt)
    return response.text
