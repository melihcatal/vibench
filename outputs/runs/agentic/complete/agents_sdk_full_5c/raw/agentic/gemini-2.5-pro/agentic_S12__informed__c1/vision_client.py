import os

from google.cloud import vision
from azure.cognitiveservices.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


def get_google_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    # The client uses GOOGLE_APPLICATION_CREDENTIALS environment variable implicitly
    return vision.ImageAnnotatorClient()


def get_azure_vision_client():
    """Initializes and returns an Azure AI Vision client."""
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Vision endpoint and key must be set in environment variables."
        )

    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
