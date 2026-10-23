from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, SafetyAnnotation


def score_image_safety(request: ImageAnalysisRequest) -> list[SafetyAnnotation]:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = [
        SafetyAnnotation(category="adult", score=safe_search_annotation.adult.value),
        SafetyAnnotation(category="spoof", score=safe_search_annotation.spoof.value),
        SafetyAnnotation(
            category="medical", score=safe_search_annotation.medical.value
        ),
        SafetyAnnotation(
            category="violence", score=safe_search_annotation.violence.value
        ),
        SafetyAnnotation(category="racy", score=safe_search_annotation.racy.value),
    ]
    return safety_scores
