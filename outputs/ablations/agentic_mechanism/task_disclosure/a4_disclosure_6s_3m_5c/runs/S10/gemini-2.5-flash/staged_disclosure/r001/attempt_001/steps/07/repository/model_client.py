import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig, HarmCategory, HarmBlockThreshold
import os

def get_model(project_id: str = None, location: str = None, model_id: str = "gemini-pro"):
    """
    Initializes Vertex AI and returns a GenerativeModel instance.

    Args:
        project_id: The Google Cloud project ID. If None, it will be fetched from the environment.
        location: The Google Cloud location. If None, it will be fetched from the environment.
        model_id: The ID of the generative model to use (e.g., "gemini-pro", "gemini-ultra").

    Returns:
        A GenerativeModel instance.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided. Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id directly.")
    if not location:
        raise ValueError("Google Cloud Location not provided. Set GOOGLE_CLOUD_LOCATION environment variable or pass location directly.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    return model

