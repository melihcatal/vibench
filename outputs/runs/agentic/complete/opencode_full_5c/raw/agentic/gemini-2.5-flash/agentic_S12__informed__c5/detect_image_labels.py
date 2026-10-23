from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, ImageLabelResult
from google.cloud import (
    vision,
)  # Google Cloud Vision SDK import is the identifying signal


def detect_image_labels(request: ImageAnalysisRequest) -> list[ImageLabelResult]:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append(
            ImageLabelResult(description=label.description, score=label.score)
        )
    return labels
