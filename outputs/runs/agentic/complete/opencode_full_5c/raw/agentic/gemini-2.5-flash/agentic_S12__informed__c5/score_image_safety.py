from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, ImageSafetyResult
from google.cloud import (
    vision,
)  # Google Cloud Vision SDK import is the identifying signal


def score_image_safety(request: ImageAnalysisRequest) -> ImageSafetyResult:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_categories = {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }

    return ImageSafetyResult(categories=safety_categories)
