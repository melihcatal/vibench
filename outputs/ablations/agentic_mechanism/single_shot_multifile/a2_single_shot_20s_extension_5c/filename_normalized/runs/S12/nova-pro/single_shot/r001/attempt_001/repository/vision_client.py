import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

def get_vision_client():
    endpoint = os.getenv('VISION_ENDPOINT')
    key = os.getenv('VISION_KEY')
    client = ImageAnalysisClient(endpoint, key)
    return client