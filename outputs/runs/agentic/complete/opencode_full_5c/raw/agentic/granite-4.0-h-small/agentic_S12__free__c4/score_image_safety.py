# score_image_safety.py
# [SAME-SCENARIO] Check an image for unsafe or policy-sensitive visual content

import os

# Provider identification (Google Cloud Vision)
PROVIDER = "Google Cloud Vision"


def is_image_safe(image_path: str) -> bool:
    """
    Evaluate whether the image contains unsafe content.
    Returns True if safe, False if unsafe.

    Args:
        image_path (str): Local filesystem path to the image.
    """
    # Load image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Use Google Vision client (credentials must be configured via environment)
    from google.cloud import vision_v1

    client = vision_v1.ImageAnnotatorClient()
    response = client.safe_search_detection(image={"content": image_bytes})

    # Simple safety check - if any detection score exceeds a threshold, mark unsafe
    unsafe_categories = ["ADULT", "VIOLENCE"]
    for annotation in response.safe_search_annotation:
        if annotation.category in unsafe_categories and annotation.score > 0.7:
            return False
    return True
