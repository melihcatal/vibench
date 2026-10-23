import os
from vertexai.preview.generative_models import GenerativeModel, Part, Image
import vertexai

def onboarding_summary(onboarding_data: dict) -> str:
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or run in a Google Cloud environment
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"))

    model = GenerativeModel("gemini-pro") # Using gemini-pro for text generation

    prompt = f"Summarize the following user onboarding data for support purposes, focusing on key milestones and any potential issues or incomplete steps:\n\n{onboarding_data}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Onboarding summary failed: {e}"
