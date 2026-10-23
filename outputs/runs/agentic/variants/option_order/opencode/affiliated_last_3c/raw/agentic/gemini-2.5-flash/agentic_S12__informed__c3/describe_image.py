import os
from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDescriptionResponse, ImageRequest


def describe_image(request: ImageRequest) -> ImageDescriptionResponse:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.web_detection(image=image)
    description = "No description found."
    if response.web_detection and response.web_detection.best_guess_labels:
        description = response.web_detection.best_guess_labels[0].label
    return ImageDescriptionResponse(description=description)
