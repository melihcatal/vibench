# score_image_safety.py
import json
import uuid
from google.cloud import vision_v1
from vision_client import VisionClient

def score_image_safety(image_path, unsafe_categories=None):
    if unsafe_categories is None:
        unsafe_categories = [
            vision_v1.SafeSearchAnnotation.Category.ADULT,
            vision_v1.SafeSearchAnnotation.Category.VIOLENCE,
            vision_v1.SafeSearchAnnotation.Category.SPOOF,
            vision_v1.SafeSearchAnnotation.Category.MEDICAL,
            vision_v1.SafeSearchAnnotation.Category.RUDE,
        ]
    client = VisionClient()
    image = client.get_image(image_path)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.service.annotate_image(request)
    annotation = response.safe_search_annotation
    unsafe = any(getattr(annotation, cat.name.lower()) in [vision_v1.Likelihood.LIKELY, vision_v1.Likelihood.VERY_LIKELY] for cat in unsafe_categories)
    return unsafe
