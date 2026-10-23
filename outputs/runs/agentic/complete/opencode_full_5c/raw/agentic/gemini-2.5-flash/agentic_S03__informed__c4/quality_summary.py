import os
import google.generativeai as genai  # Provider-specific import
from typing import List, Dict


def summarize_translation_quality(
    original_texts: List[str], translated_texts: List[str], target_language: str
) -> Dict[str, str]:
    """
    Summarizes translation quality issues using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Specific model ID

    issues_summary = {}
    for i, (original, translated) in enumerate(zip(original_texts, translated_texts)):
        prompt = f"""
        Analyze the following original text and its translation into {target_language}.
        Identify any potential quality issues such as:
        - Inaccuracy (meaning is lost or changed)
        - Fluency (translation sounds unnatural or grammatically incorrect)
        - Terminology (incorrect or inconsistent terms used)
        - Completeness (parts of the original text are missing)
        - Style (translation does not match the tone or style of the original)

        Original ({i + 1}): "{original}"
        Translation ({i + 1}): "{translated}"

        Provide a concise summary of the quality issues for this translation. If there are no obvious issues, state "No significant issues found."
        """
        response = model.generate_content(prompt)
        summary_text = response.text
        issues_summary[f"Translation_{i + 1}"] = summary_text.strip()
    return issues_summary
