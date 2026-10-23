from vision_client import VisionClient, ImageRequest
from vision_models import SafetyDetectionResponse
from google.cloud import vision


def score_image_safety(image_request: ImageRequest) -> SafetyDetectionResponse:
    client = VisionClient()
    image = client.get_image_source(image_request)

    if isinstance(image, vision.ImageSource):
        response = client.get_client().safe_search_detection(
            image=vision.Image(source=image)
        )
    else:
        response = client.get_client().safe_search_detection(image=image)

    safe_search_annotation = response.safe_search_annotation
    safety_annotations = {
        "adult": vision.Likelihood(safe_search_annotation.adult).name,
        "spoof": vision.Likelihood(safe_search_annotation.spoof).name,
        "medical": vision.Likelihood(safe_search_annotation.medical).name,
        "violence": vision.Likelihood(safe_search_annotation.violence).name,
        "racy": vision.Likelihood(safe_search_annotation.racy).name,
    }

    return SafetyDetectionResponse(safety_annotations=safety_annotations)
