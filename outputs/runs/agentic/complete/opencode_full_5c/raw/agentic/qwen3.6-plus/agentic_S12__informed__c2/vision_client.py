import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT", "")
AZURE_VISION_KEY = os.environ.get("AZURE_VISION_KEY", "")


def get_vision_client():
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY must be set")
    credential = AzureKeyCredential(AZURE_VISION_KEY)
    client = ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT,
        credential=credential,
    )
    return client


def get_vision_endpoint():
    return AZURE_VISION_ENDPOINT


def get_vision_key():
    return AZURE_VISION_KEY
