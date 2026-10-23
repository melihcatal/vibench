import os
from typing import Optional
from google.cloud import vision_v1
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_google_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initialize and return Google Cloud Vision client."""
    return vision_v1.ImageAnnotatorClient()


def get_azure_form_recognizer_client() -> DocumentAnalysisClient:
    """Initialize and return Azure Form Recognizer client."""
    endpoint = get_azure_form_recognizer_endpoint()
    credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
    return DocumentAnalysisClient(endpoint, credential)


def get_azure_form_recognizer_endpoint() -> str:
    """Return Azure Form Recognizer endpoint."""
    return os.getenv(
        "AZURE_FORM_RECOGNIZER_ENDPOINT",
        "https://<your-resource-name>.cognitiveservices.azure.com/",
    )


def load_config() -> dict:
    """Load configuration from environment variables."""
    return {
        "google_vision_enabled": os.getenv("GOOGLE_VISION_ENABLED", "false").lower()
        == "true",
        "azure_form_recognizer_enabled": os.getenv(
            "AZURE_FORM_RECOGNIZER_ENABLED", "false"
        ).lower()
        == "true",
    }
