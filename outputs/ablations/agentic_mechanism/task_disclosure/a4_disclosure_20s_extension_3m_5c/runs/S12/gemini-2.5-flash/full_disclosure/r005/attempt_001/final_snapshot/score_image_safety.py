import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

def score_image_safety(image_path: str):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A dictionary containing the safety annotation results.
    """
    client = vision_v1.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Google Cloud Vision API will be identifiable by 'google.cloud.vision_v1' and 'ImageAnnotatorClient'
    # and the specific response structure 'safe_search_annotation'.

    return {
        "adult": safe_search_annotation.adult,
        "spoof": safe_search_annotation.spoof,
        "medical": safe_search_annotation.medical,
        "violence": safe_search_annotation.violence,
        "racy": safe_search_annotation.racy,
    }
