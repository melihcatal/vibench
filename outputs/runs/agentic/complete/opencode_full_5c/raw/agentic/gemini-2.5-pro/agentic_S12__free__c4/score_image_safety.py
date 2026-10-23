from google.cloud import vision
from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse, ImageSafety


def score_image_safety(request: VisionRequest) -> VisionResponse:
    """Scores the safety of an image."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = [
        ImageSafety(
            "adult", vision.Likelihood(safe_search.adult).name, safe_search.adult
        ),
        ImageSafety(
            "medical", vision.Likelihood(safe_search.medical).name, safe_search.medical
        ),
        ImageSafety(
            "spoof", vision.Likelihood(safe_search.spoof).name, safe_search.spoof
        ),
        ImageSafety(
            "violence",
            vision.Likelihood(safe_search.violence).name,
            safe_search.violence,
        ),
        ImageSafety("racy", vision.Likelihood(safe_search.racy).name, safe_search.racy),
    ]

    return VisionResponse(safety_scores=safety_scores)
