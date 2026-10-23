import os
from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageTextResponse, ImageRequest


def detect_image_text(request: ImageRequest) -> ImageTextResponse:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    # The first text annotation is usually the full text detected in the image
    full_text = texts[0] if texts else ""
    return ImageTextResponse(text=full_text)
