from vision_client import get_google_vision_client
from vision_models import ImageLabel, ImageLabels
from google.cloud import vision


def detect_image_labels(image_uri: str) -> ImageLabels:
    client = get_google_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = [
        ImageLabel(label=label.description, score=label.score) for label in labels
    ]

    return ImageLabels(labels=detected_labels)
