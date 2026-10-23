import os
from google.cloud import vision


def score_image_safety(image_path):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    if response.error.message:
        raise Exception(f"Google Cloud Vision error: {response.error.message}")

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
            safe_search.violence <= vision.Likelihood.POSSIBLE,
            safe_search.racy <= vision.Likelihood.POSSIBLE,
        ]
    )

    return {
        "safety_scores": safety_scores,
        "is_safe": is_safe,
        "overall_risk": "HIGH" if not is_safe else "LOW",
    }
