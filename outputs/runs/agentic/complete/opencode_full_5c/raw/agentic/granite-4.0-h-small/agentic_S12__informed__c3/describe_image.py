import os
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a concise description for an image using Google Cloud Vision.

    Args:
        image_path: Path to the input image file.

    Returns:
        A short visual description string.
    """
    client = VisionClient(service="google-cloud-vision")
    response = client.annotate_image(
        image_path, features=["OBJECT_LOCALIZATION", "TEXT_DETECTION"]
    )  # simplified
    description = response.get("description", "")
    # Fallback to textual OCR if present
    if description == "":
        description = response.get("text", "")
    return description.strip()
