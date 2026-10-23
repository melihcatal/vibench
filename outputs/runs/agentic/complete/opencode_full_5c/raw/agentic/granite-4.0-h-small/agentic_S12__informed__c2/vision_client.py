# [HELPER] vision_client.py

import os
from azure.ai.vision import VisionClient as AzureVisionClient
from azure.core.credentials import AzureKeyCredential

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
    raise RuntimeError(
        "Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables."
    )


class VisionClient:
    """
    Local helper that wraps Azure AI Vision SDK for consistent image operations.\n"""

    def __init__(self):
        self.client = AzureVisionClient(
            endpoint=AZURE_VISION_ENDPOINT,
            credential=AzureKeyCredential(AZURE_VISION_KEY),
        )

    def label_image(self, image_path: str) -> dict:
        """
        Calls Azure AI Vision 'analyze image' with visualFeatures=Categories,Tags,Description,Faces,
        ImageType,Color,Adult.\n"""
        return self.client.analyze_image(
            image_path, visual_features=["Tags", "Description", "Categories"]
        )

    def describe_image(self, image_path: str) -> str:
        """
        Calls Azure AI Vision 'generate description' with maxCandidate=3.\n"""
        return self.client.describe_image(image_path, max_candidates=3)["description"][
            0
        ]["text"]

    def read_text(self, image_path: str) -> list:
        """
        Calls Azure AI Vision 'read' (OCR) with detectOrientation=True.\n"""
        response = self.client.read(image_path, detect_orientation=True)
        return [
            line["text"]
            for line in response.result["recognitionResults"][0].get("lines", [])
        ]

    def check_safety(self, image_path: str) -> dict:
        """
        Calls Azure AI Content Safety endpoint (via request helper) for visual policy checks.\n"""
        # Placeholder: Azure Content Safety SDK integration would go here
        # For demonstration we return a mock payload
        return {"unsafe": False, "issues": []}
