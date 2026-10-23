from google.cloud import vision
from vision_client import get_vision_client
from typing import Dict, Any

def score_image_safety(image_content: bytes) -> Dict[str, Any]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.
    Returns scores for various safety categories.
    """
    client = get_vision_client()
    image = vision.Image(content=image_content)
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Convert likelihood enum to a more readable string or score
    likelihood_map = {
        vision.Likelihood.UNKNOWN: "UNKNOWN",
        vision.Likelihood.VERY_UNLIKELY: "VERY_UNLIKELY",
        vision.Likelihood.UNLIKELY: "UNLIKELY",
        vision.Likelihood.POSSIBLE: "POSSIBLE",
        vision.Likelihood.LIKELY: "LIKELY",
        vision.Likelihood.VERY_LIKELY: "VERY_LIKELY",
    }

    safety_scores = {
        "adult": likelihood_map.get(safe_search_annotation.adult, "UNKNOWN"),
        "spoof": likelihood_map.get(safe_search_annotation.spoof, "UNKNOWN"),
        "medical": likelihood_map.get(safe_search_annotation.medical, "UNKNOWN"),
        "violence": likelihood_map.get(safe_search_annotation.violence, "UNKNOWN"),
        "racy": likelihood_map.get(safe_search_annotation.racy, "UNKNOWN"),
    }
    return safety_scores
