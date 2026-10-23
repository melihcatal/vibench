from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageText


def detect_text(image_uri: str) -> list[ImageText]:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0]
        return [ImageText(text=full_text.description, locale=full_text.locale)]
    return []
