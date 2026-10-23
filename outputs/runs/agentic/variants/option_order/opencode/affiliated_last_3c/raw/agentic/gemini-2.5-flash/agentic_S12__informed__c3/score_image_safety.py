import os
from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageSafetyResponse, ImageRequest


def score_image_safety(request: ImageRequest) -> ImageSafetyResponse:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search_annotations = {
        "adult": response.safe_search_annotation.adult.name,
        "medical": response.safe_search_annotation.medical.name,
        "racy": response.safe_search_annotation.racy.name,
        "spoof": response.safe_search_annotation.spoof.name,
        "violence": response.safe_search_annotation.violence.name,
    }
    return ImageSafetyResponse(safe_search_annotations=safe_search_annotations)
