import os
from google.cloud import vision
from google.cloud import documentai_v1 as documentai

def get_vision_client() -> vision.ImageAnnotatorClient:
    """Provides a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()

def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    """Provides a Google Cloud Document AI client."""
    return documentai.DocumentProcessorServiceClient()

def get_project_id() -> str:
    """Retrieves the Google Cloud Project ID from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

def get_documentai_location() -> str:
    """Retrieves the Google Cloud Document AI location from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
