import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_vision_client():
    endpoint = os.environ.get("VISION_ENDPOINT")
    key = os.environ.get("VISION_KEY")

    if not endpoint or not key:
        raise ValueError("VISION_ENDPOINT and VISION_KEY environment variables must be set.")

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
    return client
