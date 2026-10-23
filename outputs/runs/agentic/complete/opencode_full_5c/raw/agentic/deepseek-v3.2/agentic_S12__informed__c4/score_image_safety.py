import os
from typing import Dict, Any
from vision_client import get_vision_client


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """
    Check an image for unsafe or policy-sensitive visual content using Amazon Rekognition.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing safety scores and moderation labels
    """
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_moderation_labels(Image={"Bytes": image_bytes})

    moderation_labels = []
    for label in response.get("ModerationLabels", []):
        moderation_labels.append(
            {
                "name": label["Name"],
                "confidence": label["Confidence"],
                "parent_name": label.get("ParentName", ""),
            }
        )

    is_safe = len(moderation_labels) == 0

    return {
        "is_safe": is_safe,
        "moderation_labels": moderation_labels,
        "safety_score": 100.0 if is_safe else 0.0,
    }
