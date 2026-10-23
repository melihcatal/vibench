from google.cloud import vision

from vision_client import vision_client
from vision_models import ensure_text


def describe_image(image_path: str):
    client = vision_client()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:5]]
    return ensure_text(", ".join(labels))
