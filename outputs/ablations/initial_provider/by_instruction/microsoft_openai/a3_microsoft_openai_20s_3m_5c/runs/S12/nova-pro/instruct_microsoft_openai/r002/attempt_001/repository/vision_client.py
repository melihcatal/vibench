import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

class VisionClient:
    def __init__(self):
        self.endpoint = os.getenv('VISION_ENDPOINT')
        self.key = os.getenv('VISION_KEY')
        self.client = ImageAnalysisClient(self.endpoint, AzureKeyCredential(self.key))

    def get_client(self):
        return self.client