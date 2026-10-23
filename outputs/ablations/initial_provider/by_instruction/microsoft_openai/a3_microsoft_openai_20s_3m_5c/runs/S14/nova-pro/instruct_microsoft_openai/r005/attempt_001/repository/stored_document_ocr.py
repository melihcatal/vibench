from azure.ai.vision.image_analysis import ImageAnalysisClient
from azure.ai.vision.image_analysis.models import VisualFeatures

class OCRClient:
    def __init__(self, endpoint, key):
        self.client = ImageAnalysisClient(endpoint, key)

    def ocr(self, image_url):
        result = self.client.analyze(image_url, visual_features=[VisualFeatures.TEXT])
        return result.text.text