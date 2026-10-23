from vision_client import VisionClient
from vision_models import (
    ImageDetectionRequest,
    ImageSafetyDetectionResponse,
    SafeSearchAnnotation,
)
from google.cloud import vision


def score_image_safety(request: ImageDetectionRequest) -> ImageSafetyDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_annotation = SafeSearchAnnotation(
        adult=vision.Likelihood(safe_search.adult).name,
        spoof=vision.Likelihood(safe_search.spoof).name,
        medical=vision.Likelihood(safe_search.medical).name,
        violence=vision.Likelihood(safe_search.violence).name,
        racy=vision.Likelihood(safe_search.racy).name,
    )

    return ImageSafetyDetectionResponse(safe_search_annotation=safety_annotation)
