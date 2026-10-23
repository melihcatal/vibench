from google.cloud import vision

from vision_client import vision_client
from vision_models import ensure_text


def detect_image_text(image_path: str):
    client = vision_client()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    return ensure_text(response.text_annotations[0].description if response.text_annotations else "")
