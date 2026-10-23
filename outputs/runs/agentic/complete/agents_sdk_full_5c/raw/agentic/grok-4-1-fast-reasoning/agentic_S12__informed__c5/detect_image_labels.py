from google.cloud import vision
from vision_client import get_google_vision_client, load_image_bytes
from vision_models import ImageLabels

def detect_image_labels(image_path: str) -> ImageLabels:
    client = get_google_vision_client()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [
        {
            "name": label.description,
            "confidence": float(label.score)
        }
        for label in response.label_annotations[:10]
    ]
    return {"labels": labels}