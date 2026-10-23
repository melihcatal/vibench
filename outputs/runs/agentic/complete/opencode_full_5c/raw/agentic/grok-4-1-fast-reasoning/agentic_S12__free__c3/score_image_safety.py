from google.cloud import vision_v1 as vision
from vision_client import image_to_bytes
from vision_models import SafetyScore
from typing import Dict


def score_image_safety(image_path: str) -> SafetyScore:
    client = vision.ImageAnnotatorClient()
    content = image_to_bytes(image_path)
    image = vision.Image(content=content)
    features = [vision.Feature(type_=vision.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request=request)
    safesearch = response.safe_search_annotation
    categories = {
        "adult": safesearch.adult.value / 5.0,
        "violence": safesearch.violence.value / 5.0,
        "racy": safesearch.racy.value / 5.0,
    }
    score = sum(categories.values()) / len(categories)
    return SafetyScore(score=score, categories=categories)
