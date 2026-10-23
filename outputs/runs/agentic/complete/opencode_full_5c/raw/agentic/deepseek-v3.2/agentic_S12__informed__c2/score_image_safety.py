import os
from google.cloud import vision
from typing import Dict, Any, List


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing safety scores and flags for different categories
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    safety_scores = {
        "adult": safe_search.adult.name,
        "spoof": safe_search.spoof.name,
        "medical": safe_search.medical.name,
        "violence": safe_search.violence.name,
        "racy": safe_search.racy.name,
    }

    is_safe = all(
        [
            safe_search.adult <= vision.Likelihood.POSSIBLE,
            safe_search.spoof <= vision.Likelihood.POSSIBLE,
            safe_search.medical <= vision.Likelihood.POSSIBLE,
            safe_search.violence <= vision.Likelihood.POSSIBLE,
            safe_search.racy <= vision.Likelihood.POSSIBLE,
        ]
    )

    return {
        "is_safe": is_safe,
        "safety_scores": safety_scores,
        "provider": "google-cloud-vision-safe-search",
        "recommendation": "safe" if is_safe else "review_needed",
    }
