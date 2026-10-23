import os
from vision_client import VisionClient

def score_image_safety(image_path: str) -> bool:
    """Check an image for unsafe or policy-sensitive visual content using Alibaba Cloud Vision API.
    Returns True if safe, False if unsafe.
    """
    with open(image_path, "rb") as img_file:
        result = VisionClient().vision_client.detect_safety(image=img_file.read())
    # The API typically returns a boolean 'safe' flag
    return result.get('safe', False)
