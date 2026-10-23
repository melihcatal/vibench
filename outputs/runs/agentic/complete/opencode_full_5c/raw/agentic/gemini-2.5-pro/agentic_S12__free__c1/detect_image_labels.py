from google.cloud import vision
from vision_client import get_vision_client
from vision_models import Label


def detect_labels(image_path: str) -> list[Label]:
    client = get_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return [Label(description=label.description, score=label.score) for label in labels]
