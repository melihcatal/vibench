import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def get_vision_client():
    endpoint = os.getenv('VISION_ENDPOINT')
    key = os.getenv('VISION_KEY')
    credential = AzureKeyCredential(key)
    client = ImageAnalysisClient(endpoint, credential)
    return client