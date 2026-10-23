import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisOptions, VisualFeatures

# Initialize the client
endpoint = os.getenv('VISION_ENDPOINT')
key = os.getenv('VISION_KEY')
client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

def detect_labels(image_path):
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data, ImageAnalysisOptions(visual_features=[VisualFeatures.OBJECTS]))
        return result.objects.objects