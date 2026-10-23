from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

def get_image_analysis_client():
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
