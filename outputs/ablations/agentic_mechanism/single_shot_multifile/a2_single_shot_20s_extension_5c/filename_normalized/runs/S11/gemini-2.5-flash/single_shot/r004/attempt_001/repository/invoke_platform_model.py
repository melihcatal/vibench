import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

def invoke_platform_model(prompt: str) -> str:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text