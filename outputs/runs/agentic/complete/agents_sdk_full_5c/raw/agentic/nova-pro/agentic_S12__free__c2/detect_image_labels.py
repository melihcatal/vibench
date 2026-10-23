import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def detect_image_labels(image_path):
    endpoint = os.getenv('VISION_ENDPOINT')
    key = os.getenv('VISION_KEY')
    client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    with open(image_path, 'rb') as image_data:
        result = client.analyze(image_data, visual_features=[VisualFeatures.OBJECTS])
        return result.objects.objects