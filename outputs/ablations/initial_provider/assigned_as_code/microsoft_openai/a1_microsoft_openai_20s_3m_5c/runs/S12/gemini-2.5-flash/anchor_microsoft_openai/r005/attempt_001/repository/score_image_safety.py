from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, SafetyDetectionResponse

def score_image_safety(payload: ImageDetectionRequest, config: dict = None) -> SafetyDetectionResponse:
    client = get_vision_client()
    image = vision.Image(content=payload.image_bytes) if payload.image_bytes else vision.Image(image_uri=payload.image_uri)

    response = client.safe_search_detection(image=image)
    safe_search_annotations = response.safe_search_annotation

    # Convert enum values to strings for easier consumption
    def get_likelihood_name(likelihood_value):
        return vision.Likelihood(likelihood_value).name

    safety_scores = {
        'adult': get_likelihood_name(safe_search_annotations.adult),
        'spoof': get_likelihood_name(safe_search_annotations.spoof),
        'medical': get_likelihood_name(safe_search_annotations.medical),
        'violence': get_likelihood_name(safe_search_annotations.violence),
        'racy': get_likelihood_name(safe_search_annotations.racy),
    }

    return SafetyDetectionResponse(safe_search_annotations=safety_scores)
