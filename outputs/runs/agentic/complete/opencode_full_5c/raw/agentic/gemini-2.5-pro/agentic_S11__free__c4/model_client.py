import os
import vertexai
from vertexai.generative_models import GenerativeModel


def get_model_client(project: str, location: str) -> GenerativeModel:
    """Initializes Vertex AI and returns a GenerativeModel client."""
    vertexai.init(project=project, location=location)
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    return model


def get_google_cloud_project():
    """Retrieves the Google Cloud project ID from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_google_cloud_location():
    """Retrieves the Google Cloud location from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
