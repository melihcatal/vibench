import os
from google.cloud import vision

def score_image_safety(image_bytes: bytes) -> dict:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API.

    Args:
        image_bytes: The image content in bytes.

    Returns:
        A dictionary containing the safety moderation scores.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation
    
    safety_scores = {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }
    
    return {'safety_scores': safety_scores}
