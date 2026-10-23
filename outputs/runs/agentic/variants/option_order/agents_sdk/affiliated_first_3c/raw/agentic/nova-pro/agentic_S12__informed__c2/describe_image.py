import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

client = ImageAnalysisClient(endpoint=os.getenv('AZURE_VISION_ENDPOINT'), credential=os.getenv('AZURE_VISION_KEY'))

def describe_image(image_path):
    with open(image_path, 'rb') as image_data:
        result = client.analyze(image_data, visual_features=[VisualFeatures.CAPTION])
        return result.caption.text