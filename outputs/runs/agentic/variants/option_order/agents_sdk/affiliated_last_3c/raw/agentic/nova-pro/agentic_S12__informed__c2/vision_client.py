import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient

def get_client():
    return ImageAnalysisClient(endpoint=os.getenv('AZURE_VISION_ENDPOINT'), credential=os.getenv('AZURE_VISION_KEY'))