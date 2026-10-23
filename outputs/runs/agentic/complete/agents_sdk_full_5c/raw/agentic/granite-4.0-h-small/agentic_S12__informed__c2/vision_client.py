import os
import azure.ai.vision.imageanalysis as vision

class VisionClient:
    def __init__(self):
        # Azure AI Vision endpoint and key are expected in env vars
        endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        key = os.getenv("AZURE_VISION_KEY")
        self._client = vision.ImageAnalysisClient(endpoint=endpoint, credential=key)
    
    def create_image_analyser(self):
        # Returns a ready‑to‑use analyser object
        return self._client.analyser()
