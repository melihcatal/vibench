import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_translation_quality(translated_text: str, source_text: str, project_id: str = None, location: str = None) -> str:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided or found in GOOGLE_CLOUD_PROJECT environment variable.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for summarization

    prompt = f"""Summarize any potential quality issues or discrepancies between the source text and its translation. Focus on accuracy, fluency, and fidelity.

Source Text: {source_text}
Translated Text: {translated_text}

Summary of Quality Issues:"""

    response = model.generate_content(prompt)
    return response.text
