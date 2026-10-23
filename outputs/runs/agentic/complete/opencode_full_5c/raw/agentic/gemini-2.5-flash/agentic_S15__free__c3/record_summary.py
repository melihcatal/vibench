import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_document_text(text_content: str, project_id: str, location: str = "us-central1") -> str:
    """
    Summarizes retrieved document records using Google Cloud Vertex AI (Generative AI).
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    prompt = f"Summarize the following text:

{text_content}

Summary:"

    response = model.generate_content(prompt)
    return response.text
