from vision_client import get_vision_client
from vision_models import *
from google.cloud import vision

def score_image_safety(image_path):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }
    return safety_scores
