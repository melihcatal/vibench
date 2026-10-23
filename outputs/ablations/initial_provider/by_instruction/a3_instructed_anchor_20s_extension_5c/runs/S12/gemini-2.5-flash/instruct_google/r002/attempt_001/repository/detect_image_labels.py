from vision_client import get_vision_client
from vision_models import *

def detect_image_labels(image_path):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    result_labels = []
    for label in labels:
        result_labels.append(label.description)

    return result_labels
