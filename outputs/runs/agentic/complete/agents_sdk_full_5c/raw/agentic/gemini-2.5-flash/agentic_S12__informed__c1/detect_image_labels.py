from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageInput, ImageLabel
import base64
from typing import List

def detect_labels_in_image(image_input: ImageInput) -> List[ImageLabel]:
    """Detects labels in the image using Google Cloud Vision."""
    client = get_vision_client()
    image = vision.Image(content=base64.b64decode(image_input.image_content_base64))

    response = client.label_detection(image=image)
    labels = [ImageLabel(description=label.description, score=label.score) for label in response.label_annotations]
    return labels
