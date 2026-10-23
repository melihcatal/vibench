from google.cloud import aiplatform_v1beta1
import os

def get_model_client(
    project_id: str = os.getenv("GCP_PROJECT_ID"),
    location: str = os.getenv("GCP_LOCATION"),
    model_name: str = "gemini-pro",
):
    """
    Returns a configured GenerativeModel client for Vertex AI.
    """
    aiplatform_v1beta1.init(project=project_id, location=location)
    return aiplatform_v1beta1.GenerativeModel(model_name)

def generate_text(
    prompt: str,
    project_id: str = os.getenv("GCP_PROJECT_ID"),
    location: str = os.getenv("GCP_LOCATION"),
    model_name: str = "gemini-pro",
    **kwargs,
) -> str:
    """
    Generates text using a hosted LLM from Vertex AI.
    """
    model = get_model_client(project_id, location, model_name)
    response = model.generate_content(prompt, **kwargs)
    return response.candidates[0].content.parts[0].text
