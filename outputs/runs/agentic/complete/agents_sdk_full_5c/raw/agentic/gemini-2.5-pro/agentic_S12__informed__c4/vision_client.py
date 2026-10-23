import os
from google.cloud import vision
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient

def get_google_vision_client() -> vision.ImageAnnotatorClient:
    """
    Initializes and returns a Google Cloud Vision client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return vision.ImageAnnotatorClient()

def get_azure_vision_client() -> ImageAnalysisClient:
    """
    Initializes and returns an Azure AI Vision client.
    """
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]
    
    return ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
