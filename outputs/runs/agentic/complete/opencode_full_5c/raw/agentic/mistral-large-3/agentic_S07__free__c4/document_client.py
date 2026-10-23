import os
from typing import Optional
from google.cloud import vision_v1
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_google_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Initialize and return Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return vision_v1.ImageAnnotatorClient()


def get_azure_form_recognizer_client() -> DocumentAnalysisClient:
    """Initialize and return Azure Form Recognizer client."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_FORM_RECOGNIZER_ENDPOINT or AZURE_FORM_RECOGNIZER_KEY not set."
        )

    return DocumentAnalysisClient(endpoint, AzureKeyCredential(key))
