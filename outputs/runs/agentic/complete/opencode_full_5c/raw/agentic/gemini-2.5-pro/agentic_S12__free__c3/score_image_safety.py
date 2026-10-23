from google.cloud import vision
from vision_client import get_vision_client
from vision_models import SafetyAnnotation


def score_image_safety(image_uri: str) -> SafetyAnnotation:
    """Scores an image for safety using Google Cloud Vision."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    return SafetyAnnotation(
        adult=vision.Likelihood(safe_search.adult).name,
        spoof=vision.Likelihood(safe_search.spoof).name,
        medical=vision.Likelihood(safe_search.medical).name,
        violence=vision.Likelihood(safe_search.violence).name,
        racy=vision.Likelihood(safe_search.racy).name,
    )
