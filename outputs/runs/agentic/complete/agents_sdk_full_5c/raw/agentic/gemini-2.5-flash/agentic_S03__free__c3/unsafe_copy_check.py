import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def check_unsafe_content(
    localized_copy: str,
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
    location: str = "us-central1",
) -> str:
    """Checks localized copy for unsafe content using Google Cloud's Generative AI (Gemini Pro)."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    prompt = f"""Analyze the following localized copy for any unsafe, harmful, hateful, sexually explicit, "\
             f"or violent content. Respond with 'SAFE' if no unsafe content is found, "\
             f"otherwise, describe the unsafe content detected.

Localized Copy: """{localized_copy}"""
Analysis:"""

    response = model.generate_content(prompt)
    return response.text
