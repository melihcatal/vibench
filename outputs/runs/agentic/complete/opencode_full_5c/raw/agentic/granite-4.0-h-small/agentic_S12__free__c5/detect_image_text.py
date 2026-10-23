# SAME-SCENARIO
# Detect text appearing inside an image using AWS Textract
import json
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detect and extract text blocks from an image.

    Args:
        image_path: Path to the image file.

    Returns:
        List of detected text strings.
    """
    client = VisionClient("aws")  # Provider identifier
    response = client.detect_text(image_path)
    texts = [
        block["Text"]
        for block in response.get("Blocks", [])
        if block.get("BlockType") == "LINE"
    ]
    return texts
