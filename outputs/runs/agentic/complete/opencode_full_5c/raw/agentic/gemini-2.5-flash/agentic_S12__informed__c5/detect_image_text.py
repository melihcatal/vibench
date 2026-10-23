from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, ImageTextResult
from google.cloud import (
    vision,
)  # Google Cloud Vision SDK import is the identifying signal


def detect_image_text(request: ImageAnalysisRequest) -> ImageTextResult:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    detected_text = ""
    if texts:
        detected_text = texts[
            0
        ].description  # The first annotation is the total text detected

    return ImageTextResult(text=detected_text)
