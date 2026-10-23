from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, TextDetectionResponse

def detect_image_text(payload: ImageDetectionRequest, config: dict = None) -> TextDetectionResponse:
    client = get_vision_client()
    image = vision.Image(content=payload.image_bytes) if payload.image_bytes else vision.Image(image_uri=payload.image_uri)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first annotation is the overall text detected in the image
        detected_text = texts[0].description
    else:
        detected_text = ""

    return TextDetectionResponse(text=detected_text)
