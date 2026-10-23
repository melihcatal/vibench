import os
from google.cloud import vision


def describe_image(image_content: bytes) -> str:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    if labels:
        return f"The image depicts: {', '.join(labels)}."
    return "No discernible description for the image."
