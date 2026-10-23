from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageDetectionRequest, SafeSearchDetectionResponse


def score_image_safety(request: ImageDetectionRequest) -> SafeSearchDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    return SafeSearchDetectionResponse(
        adult=safe_search_annotation.adult.name,
        spoof=safe_search_annotation.spoof.name,
        medical=safe_search_annotation.medical.name,
        violence=safe_search_annotation.violence.name,
        racy=safe_search_annotation.racy.name,
    )
