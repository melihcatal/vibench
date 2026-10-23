import os
from google.cloud import vision


def score_image_safety(image_content: bytes) -> dict:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation
    return {
        "adult": safe_search.adult.name,
        "spoof": safe_search.spoof.name,
        "medical": safe_search.medical.name,
        "violence": safe_search.violence.name,
        "racy": safe_search.racy.name,
    }
