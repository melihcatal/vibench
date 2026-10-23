import os
from typing import Dict, Any
from google.cloud import vision


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """
    Check an image for unsafe or policy-sensitive visual content using Google Cloud Vision.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing safety scores and flags
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    safety_categories = {
        "adult": safe_search.adult.name,
        "spoof": safe_search.spoof.name,
        "medical": safe_search.medical.name,
        "violence": safe_search.violence.name,
        "racy": safe_search.racy.name,
    }

    is_safe = all(
        category in ["VERY_UNLIKELY", "UNLIKELY"]
        for category in safety_categories.values()
    )

    return {
        "is_safe": is_safe,
        "safety_scores": safety_categories,
        "adult_score": safe_search.adult.name,
        "violence_score": safe_search.violence.name,
        "racy_score": safe_search.racy.name,
        "medical_score": safe_search.medical.name,
        "spoof_score": safe_search.spoof.name,
    }
