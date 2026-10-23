import io
from google.cloud import vision
from vision_client import load_image_bytes


def detect_labels(image_path: str) -> list[str]:
    client = vision.ImageAnnotatorClient()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:20]]
    return labels
