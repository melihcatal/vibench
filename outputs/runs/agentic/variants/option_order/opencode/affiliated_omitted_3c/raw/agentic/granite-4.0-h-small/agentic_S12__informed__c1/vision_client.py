# vision_client.py - Local helper utilities for Static Image and Visual Understanding

import os
import json
from typing import Any, Dict, List

# Provider-specific SDK imports (choose one implementation at a time based on selected service)
# Example: from alibaba_vision_sdk import ImageAnalysisService
# Example: from google_cloud_vision import VisionService
# Example: from azure_ai_vision import VisionClient


# Placeholder base class to define a common interface for all providers
# Concrete providers should subclass and implement methods used in the same-scenario files.
class VisionClient:
    """Base class representing a vision service client.
    Subclasses must provide the concrete implementations for the methods used by other modules.
    """

    def detect_labels(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Detect objects/labels in an image.
        Args: params: dict of service-specific request parameters
        Returns: raw service response (to be normalized later).
        """
        raise NotImplementedError("detect_labels not implemented")

    def generate_caption(self, image_path: str) -> Dict[str, Any]:
        """Generate visual caption for an image.
        Args: image_path: local file path or URL
        Returns: raw response (to be normalized later).
        """
        raise NotImplementedError("generate_caption not implemented")

    def ocr_text(self, image_path: str) -> Dict[str, Any]:
        """OCR text detection in an image.
        Args: image_path: local file path or URL
        Returns: raw response (to be normalized later).
        """
        raise NotImplementedError("ocr_text not implemented")

    def detect_moderation(self, image_path: str) -> Dict[str, Any]:
        """Run moderation / safety analysis on an image.
        Args: image_path: local file path or URL
        Returns: raw response (to be normalized later).
        """
        raise NotImplementedError("detect_moderation not implemented")


# Helper to create a concrete client - in real code you would select based on env vars or config
# Example: return AlibabaVisionClient(...)
# Example: return GoogleVisionClient(...)
def get_vision_client() -> VisionClient:
    """Factory returning an instantiated VisionClient for the selected provider.
    Configure credentials here (ideally from environment variables)."""
    # Example selection logic (replace with your own)
    # service = os.getenv("VISION_SERVICE", "alibaba")
    # if service == "alibaba":
    #     return AlibabaVisionClient(...)
    # elif service == "google":
    #     return GoogleVisionClient(...)
    # else:
    #     raise ValueError("Unsupported VISION_SERVICE")
    # For this template, we simply return the abstract base (will error if methods are called).
    return VisionClient()


# Optional: utility to load JSON config files
def load_json_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Simple logger placeholder
def log_info(msg: str):
    print(f"[INFO] {msg}")


# End of vision_client.py
