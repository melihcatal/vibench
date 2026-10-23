import os
from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageLabelResponse, ImageRequest


def detect_image_labels(request: ImageRequest) -> ImageLabelResponse:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return ImageLabelResponse(labels=labels)
