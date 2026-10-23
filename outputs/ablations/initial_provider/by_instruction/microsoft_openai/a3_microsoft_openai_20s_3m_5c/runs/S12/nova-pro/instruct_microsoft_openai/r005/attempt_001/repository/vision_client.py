from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

class VisionClient:
    def __init__(self, endpoint, key):
        self.client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

    def analyze_image(self, image_url, features):
        return self.client.analyze(image_url, visual_features=features)