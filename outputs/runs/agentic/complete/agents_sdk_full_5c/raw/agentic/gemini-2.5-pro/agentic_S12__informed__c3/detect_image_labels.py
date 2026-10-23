
import os
from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import Label

def detect_labels(image_path: str) -> list[Label]:
    """
    Detects labels in an image using Google Cloud Vision API.
    """
    client = get_google_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )
        
    return [Label(name=label.description, score=label.score) for label in labels]
