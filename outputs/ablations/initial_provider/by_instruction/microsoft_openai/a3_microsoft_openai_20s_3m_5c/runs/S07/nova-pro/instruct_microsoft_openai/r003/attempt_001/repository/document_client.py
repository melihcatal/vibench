from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisMode
from azure.core.credentials import AzureKeyCredential

class DocumentClient:
    def __init__(self, endpoint, api_key):
        self.client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    def analyze(self, image_data, mode):
        return self.client.analyze(image_data, visual_features=[mode])