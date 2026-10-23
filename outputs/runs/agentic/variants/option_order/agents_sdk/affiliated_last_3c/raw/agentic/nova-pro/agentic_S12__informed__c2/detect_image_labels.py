import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

client = ImageAnalysisClient(endpoint=os.getenv('AZURE_VISION_ENDPOINT'), credential=os.getenv('AZURE_VISION_KEY'))

def detect_labels(image_path):
    with open(image_path, 'rb') as image_data:
        result = client.analyze_image(image_data, visual_features=[VisualFeatures.OBJECTS])
        return result.objects.objects