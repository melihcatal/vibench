import os

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_record(text_content: str, project_id: str, location: str = "us-central1") -> str:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize the following document: {text_content}")
    return response.text
