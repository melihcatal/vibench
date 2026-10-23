import os
from google.cloud import vision
from vision_client import get_vision_client


def score_image_safety(image_path):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    safety_scores = {
        "adult": safe.adult.name,
        "spoof": safe.spoof.name,
        "medical": safe.medical.name,
        "violence": safe.violence.name,
        "racy": safe.racy.name,
    }

    is_safe = all(
        [
            safe.adult <= vision.Likelihood.POSSIBLE,
            safe.spoof <= vision.Likelihood.POSSIBLE,
            safe.medical <= vision.Likelihood.POSSIBLE,
            safe.violence <= vision.Likelihood.POSSIBLE,
            safe.racy <= vision.Likelihood.POSSIBLE,
        ]
    )

    return {
        "safety_scores": safety_scores,
        "is_safe": is_safe,
        "adult_score": safe.adult.value,
        "violence_score": safe.violence.value,
        "racy_score": safe.racy.value,
    }
