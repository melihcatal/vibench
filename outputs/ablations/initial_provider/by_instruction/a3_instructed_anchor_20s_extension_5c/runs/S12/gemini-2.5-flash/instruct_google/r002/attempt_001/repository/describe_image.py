from vision_client import get_vision_client
from vision_models import *
from google.cloud import vision # Explicitly import vision for type hinting and clarity

def describe_image(image_path):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        descriptions = [label.description for label in labels]
        return ", ".join(descriptions)
    else:
        return "No clear description found."
