# [SAME-SCENARIO] score_image_safety.py

import os
from vision_client import VisionClient


def score_image_safety(image_path: str) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content using Azure AI Content Safety SDK.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Evaluation result indicating safety status and detected issues.
    """
    client = VisionClient()
    return client.check_safety(image_path)
