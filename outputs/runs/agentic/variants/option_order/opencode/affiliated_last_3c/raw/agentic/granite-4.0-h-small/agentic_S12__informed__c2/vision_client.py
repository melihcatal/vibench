# vision_client.py
"""Local helper utilities for Static Image and Visual Understanding integration.

Provides a thin wrapper around a concrete provider (Azure AI Vision) and normalizes its
response formats to a simpler, provider‑agnostic structure.  Other steps may reuse this
client or create specialized helpers as needed."

import os
from typing import Any, Dict, List
from dotenv import load_dotenv

load_dotenv()  # loads AZURE_VISION_ENDPOINT, AZURE_VISION_KEY from .env

class VisionClient:
    """Client wrapper for Azure AI Vision services."""

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        self.key = os.getenv("AZURE_VISION_KEY")
        # placeholder: instantiate the real SDK client here
        # from azure.ai.vision import ImageAnalysisClient
        # self.client = ImageAnalysisClient(endpoint=self.endpoint, credential=self.key)

    def _call(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call the underlying Azure SDK method and return JSON response."""
        # Placeholder implementation – replace with real SDK call when available
        # response = getattr(self.client, method)(**payload)
        # return response.to_dict()
        return {
            "dummy": "response"
        }

    def label_image(self, image_path: str) -> Dict[str, Any]:
        """Detect labels/objects in an image."""
        payload = {"imageFile": image_path}
        return self._call("label_image", payload)

    def describe(self, image_path: str) -> Dict[str, Any]:
        """Generate a short description of an image."""
        payload = {"imageFile": image_path}
        return self._call("describe", payload)

    def detect_text(self, image_path: str) -> Dict[str, Any]:
        """Detect embedded text in an image."""
        payload = {"imageFile": image_path}
        return self._call("detect_text", payload)

    def safety_check(self, image_path: str) -> Dict[str, Any]:
        """Check image safety / content policy compliance."""
        payload = {"imageFile": image_path}
        return self._call("safety_check", payload)
