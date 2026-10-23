from google.cloud import vision
from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse, ImageClassification


def detect_labels(request: VisionRequest) -> VisionResponse:
    """Detects labels in the image."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    labels = [
        ImageClassification(label=label.description, score=label.score)
        for label in response.label_annotations
    ]
    return VisionResponse(labels=labels)
