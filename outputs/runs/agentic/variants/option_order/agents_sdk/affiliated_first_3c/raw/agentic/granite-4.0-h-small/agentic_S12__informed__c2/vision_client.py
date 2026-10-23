# vision_client.py
import os
from azure.ai.vision import VisionClient as AzureVisionClient
from azure.ai.vision.models import AnalyzeImageResult
import configparser

# Load Azure credentials from environment
AZURE_VISION_ENDPOINT = os.getenv('AZURE_VISION_ENDPOINT')
AZURE_VISION_KEY = os.getenv('AZURE_VISION_KEY')

if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
    raise RuntimeError('Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables')

class VisionClient:
    def __init__(self):
        self.az_client = AzureVisionClient(endpoint=AZURE_VISION_ENDPOINT, credential=AZURE_VISION_KEY)

    # Core SDK calls forwarded to Azure
    def analyze_image_labels(self, image_path: str, **kwargs) -> AnalyzeImageResult:
        return self.az_client.analyze_image_labels(image_path, **kwargs)

    def describe_image(self, image_path: str, **kwargs) -> AnalyzeImageResult:
        return self.az_client.describe_image(image_path, **kwargs)

    def read_text(self, image_path: str, mode: str = 'Printed', **kwargs):
        # Use OCR endpoint for text detection
        return self.az_client.read_text(image_path, mode=mode, **kwargs)

    def analyze_safety(self, image_path: str, **kwargs):
        # Safety analysis endpoint (e.g., Content Safety service)
        return self.az_client.analyze_safety(image_path, **kwargs)
