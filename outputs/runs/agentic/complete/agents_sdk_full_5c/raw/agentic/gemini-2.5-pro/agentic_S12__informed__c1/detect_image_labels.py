from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import ImageLabel


def detect_labels(image_uri: str) -> list[ImageLabel]:
    """Detects labels in the image located at the given URI."""
    client = get_google_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    labels = [
        ImageLabel(name=label.description, score=label.score)
        for label in response.label_annotations
    ]
    return labels
