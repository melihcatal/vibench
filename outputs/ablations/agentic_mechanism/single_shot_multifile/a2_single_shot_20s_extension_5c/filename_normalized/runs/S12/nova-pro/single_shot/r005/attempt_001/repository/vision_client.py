import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

def get_vision_client():
    endpoint = os.getenv('VISION_ENDPOINT')
    key = os.getenv('VISION_KEY')
    return ImageAnalysisClient(endpoint, key)

def get_vision_client_with_features(features):
    client = get_vision_client()
    visual_features = [getattr(VisualFeatures, feature.upper()) for feature in features]
    return client, visual_features