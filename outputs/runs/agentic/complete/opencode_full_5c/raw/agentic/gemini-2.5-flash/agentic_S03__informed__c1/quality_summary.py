from translation_client import get_gemini_client
import os


def summarize_translation_quality_issues(
    translated_text: str, original_text: str, language: str
) -> str:
    genai = get_gemini_client()
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro model ID
    prompt = f"""Summarize any potential quality issues in the following translation from original text to {language}. Focus on accuracy, fluency, and cultural appropriateness.

Original Text: {original_text}
Translated Text: {translated_text}

Summary of quality issues:"""

    response = model.generate_content(prompt)
    return response.text
