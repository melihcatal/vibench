# SAME-SCENARIO
# Check an image for unsafe or policy-sensitive visual content using AWS Rekognition Content Moderation
import json
from vision_client import VisionClient


def score_image_safety(image_path: str) -> dict:
    """Assess image safety and return unsafe flags.

    Args:
        image_path: Path to the image file.

    Returns:
        Dict with safety verdict and details.
    """
    client = VisionClient("aws")  # Provider identifier
    response = client.moderate_content(image_path)
    unsafe = any(
        item.get("IsUnsafe", False) for item in response.get("ModerationLabels", [])
    )
    return {"unsafe": unsafe, "labels": response.get("ModerationLabels")}
