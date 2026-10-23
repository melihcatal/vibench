# SAME-SCENARIO
# Generate a short visual description for an image using Vision API
import json
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a concise description of the image content.

    Args:
        image_path: Local file path to the image.

    Returns:
        A short textual description.
    """
    client = VisionClient("vision")  # Provider identifier
    response = client.describe(image_path)
    # Use first caption or generate summary
    caption = response.get("Description", "")
    return caption if caption else "No description available"
