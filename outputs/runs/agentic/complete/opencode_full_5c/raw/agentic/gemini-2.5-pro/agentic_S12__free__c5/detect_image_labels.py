from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageLabel


def detect_labels(image_uri: str) -> list[ImageLabel]:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return [
        ImageLabel(description=label.description, score=label.score) for label in labels
    ]
