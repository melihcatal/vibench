import os

import vertexai
from vertexai.generative_models import GenerativeModel


def extract_fields(text: str):
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))
    model = GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Extract structured fields from this OCR text:\n{text}")
    return response.text
