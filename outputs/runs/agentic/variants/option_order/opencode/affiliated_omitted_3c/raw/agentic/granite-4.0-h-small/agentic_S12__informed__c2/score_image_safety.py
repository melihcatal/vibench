import os
from vision_client import VisionClient


def score_image_safety(image_path: str) -> bool:
    """Check an image for unsafe or policy‑sensitive visual content using Azure AI Content Safety.
    Returns True if safe, False otherwise.
    """
    client = VisionClient()
    safe = client.safe_content_check(image_path)
    return safe
