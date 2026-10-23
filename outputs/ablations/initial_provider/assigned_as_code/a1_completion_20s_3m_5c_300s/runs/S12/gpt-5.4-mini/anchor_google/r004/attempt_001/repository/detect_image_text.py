from google.cloud import vision

from vision_client import build_image, get_vision_client
from vision_models import normalize_text_annotations


def detect_image_text(payload, config=None):
    client = get_vision_client()
    response = client.text_detection(image=build_image(payload))
    if response.error.message:
        raise RuntimeError(response.error.message)
    texts = normalize_text_annotations(response.text_annotations)
    return {"text": texts}
