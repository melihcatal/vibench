from google.cloud import vision

from vision_client import get_vision_client, make_image
from vision_models import normalize_text_annotation


def detect_image_text(image_path=None, image_uri=None):
    client = get_vision_client()
    image = make_image(image_path=image_path, image_uri=image_uri)
    response = client.text_detection(image=image)
    return [normalize_text_annotation(text) for text in response.text_annotations]
