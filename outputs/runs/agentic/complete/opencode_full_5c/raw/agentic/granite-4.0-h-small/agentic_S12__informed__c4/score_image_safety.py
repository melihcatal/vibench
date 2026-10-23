import os
from vision_client import VisionClient


def score_image_safety(image_path: str) -> bool:
    """Check an image for unsafe or policy‑sensitive visual content using Anthropic.

    Args:
        image_path: Local file path to the image.

    Returns:
        True if safe, False otherwise.
    """
    client = VisionClient(service="anthropic")
    is_safe = client.check_safety(image_path)
    return is_safe
