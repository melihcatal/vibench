import os
from google.cloud import vision
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_google_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()


def get_azure_vision_client():
    """Initializes and returns an Azure AI Vision client."""
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Vision endpoint and key must be set as environment variables."
        )

    client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    return client
