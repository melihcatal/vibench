import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    target_language: str,
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
    location: str = "us-central1",
) -> str:
    """Summarizes translation quality issues using Google Cloud's Generative AI (Gemini Pro)."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    prompt = f"""Analyze the quality of the following translation from the source text to {target_language}. "\
             f"Identify any potential issues such as inaccuracies, unnatural phrasing, grammatical errors, "\
             f"or cultural insensitivities. Provide a concise summary of the quality issues found.

Source Text: """{source_text}"""
Translated Text: """{translated_text}"""
Summary of Quality Issues:"""

    response = model.generate_content(prompt)
    return response.text
