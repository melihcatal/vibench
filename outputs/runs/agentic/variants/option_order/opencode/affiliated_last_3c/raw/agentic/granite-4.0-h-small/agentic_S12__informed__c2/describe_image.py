# describe_image.py
import json
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a concise description for a static image using a concrete provider.

    Uses Google Cloud Vision SDK for demonstration.
    """
    client = VisionClient()
    result = client.describe(image_path)
    # Use description field if present, otherwise fallback to localized description
    description = result.get("description") or result.get("localizedDescription") or ""
    return description
