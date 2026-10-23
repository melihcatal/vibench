from google.cloud import vision
from vision_client import get_vision_client

def detect_image_labels(image_content: bytes) -> list[str]:
    """Detects labels in the image content using Google Cloud Vision AI."""
    client = get_vision_client()
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations if label.description]
    return labels
