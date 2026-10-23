import os
from azure.ai.vision import VisionClient, VisionConfiguration

class ImageVisionClient:
    """Local helper that wraps Azure AI Vision SDK and provides a uniform interface for same-scenario functions."""

    def __init__(self):
        # Load credentials from standard Azure environment variables
        endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        key = os.getenv("AZURE_VISION_KEY")
        if not endpoint or not key:
            raise RuntimeError("Azure Vision credentials (AZURE_VISION_ENDPOINT, AZURE_VISION_KEY) must be set")
        config = VisionConfiguration(endpoint=endpoint, credential=key)
        self.client = VisionClient(configuration=config)

    def analyze_image(self, image_path: str, features) -> dict:
        """Azure Vision analyze_image API wrapper."""
        with open(image_path, "rb") as img:
            return self.client.analyze_image(img, visual_features=features)

    def describe_image(self, image_path: str, max_candidates: int = 1) -> dict:
        """Azure Vision describe_image API wrapper."""
        with open(image_path, "rb") as img:
            return self.client.describe_image(img, max_candidates=max_candidates)

    def read_text(self, image_path: str, mode: str = "Printed") -> dict:
        """Azure Vision read_text API wrapper."""
        with open(image_path, "rb") as img:
            return self.client.read_text(img, mode=mode)

    def check_content_safety(self, image_path: str) -> dict:
        """Azure Content Safety moderate_content API wrapper."""
        with open(image_path, "rb") as img:
            return self.client.moderate_content(img)
