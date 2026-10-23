"""
vision_client.py - Local configuration and client helper utilities
for Static Image and Visual Understanding with Azure AI Vision.
"""

import os
from typing import Optional, Dict, Any

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


AZURE_VISION_ENDPOINT_ENV = "AZURE_VISION_ENDPOINT"
AZURE_VISION_KEY_ENV = "AZURE_VISION_KEY"


def get_azure_vision_endpoint() -> str:
    """Retrieve the Azure AI Vision service endpoint from environment."""
    endpoint = os.environ.get(AZURE_VISION_ENDPOINT_ENV)
    if not endpoint:
        raise RuntimeError(
            f"Missing required environment variable: {AZURE_VISION_ENDPOINT_ENV}"
        )
    return endpoint.rstrip("/")


def get_azure_vision_key() -> str:
    """Retrieve the Azure AI Vision API key from environment."""
    key = os.environ.get(AZURE_VISION_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"Missing required environment variable: {AZURE_VISION_KEY_ENV}"
        )
    return key


def create_image_analysis_client() -> ImageAnalysisClient:
    """Create and return an authenticated Azure AI Vision ImageAnalysisClient."""
    endpoint = get_azure_vision_endpoint()
    key = get_azure_vision_key()
    credential = AzureKeyCredential(key)
    return ImageAnalysisClient(endpoint=endpoint, credential=credential)


def build_client_config() -> Dict[str, Any]:
    """Build a configuration dictionary for Azure AI Vision."""
    return {
        "provider": "azure_ai_vision",
        "endpoint": get_azure_vision_endpoint(),
        "service": "Azure AI Vision",
    }


def validate_image_path(image_path: str) -> str:
    """Validate that the image path exists and return the absolute path."""
    resolved = os.path.abspath(image_path)
    if not os.path.isfile(resolved):
        raise FileNotFoundError(f"Image file not found: {resolved}")
    return resolved


def read_image_bytes(image_path: str) -> bytes:
    """Read an image file and return its raw bytes."""
    resolved = validate_image_path(image_path)
    with open(resolved, "rb") as f:
        return f.read()
