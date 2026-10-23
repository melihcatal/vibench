import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def summarize_record(record_content: str, model_name: str = "gemini-pro"):
    """Summarizes retrieved document records using Google Cloud Generative AI."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)

    model = GenerativeModel(model_name)
    prompt = f"Summarize the following document content:

{record_content}

Summary:"

    response = model.generate_content(prompt)
    return {"status": "success", "summary": response.text}
