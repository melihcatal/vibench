
import os
from google.cloud import vision
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Google Cloud Vision Client
def get_google_vision_client():
    """Returns a Google Cloud Vision ImageAnnotatorClient."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    return vision.ImageAnnotatorClient()

# Azure AI Vision Client
def get_azure_vision_client():
    """Returns an Azure AI Vision ImageAnalysisClient."""
    azure_vision_endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    azure_vision_key = os.environ.get("AZURE_VISION_KEY")

    if not azure_vision_endpoint or not azure_vision_key:
        raise ValueError("Azure Vision endpoint and key must be set in environment variables (AZURE_VISION_ENDPOINT, AZURE_VISION_KEY).")

    return ImageAnalysisClient(
        endpoint=azure_vision_endpoint,
        credential=AzureKeyCredential(azure_vision_key)
    )
