from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, SafeSearchDetectionResponse


def score_image_safety(request: ImageDetectionRequest) -> SafeSearchDetectionResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_content)
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Map likelihood enum to strings for easier interpretation
    likelihood_name = [
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    ]

    adult = likelihood_name[safe_search_annotation.adult]
    spoof = likelihood_name[safe_search_annotation.spoof]
    medical = likelihood_name[safe_search_annotation.medical]
    violence = likelihood_name[safe_search_annotation.violence]
    racy = likelihood_name[safe_search_annotation.racy]

    return SafeSearchDetectionResponse(
        adult=adult, spoof=spoof, medical=medical, violence=violence, racy=racy
    )
