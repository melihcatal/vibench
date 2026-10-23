from google.cloud import vision_v1
import os

def detect_labels(image_path):
    """Detects labels in the image using Google Cloud Vision API."""
    client = vision_v1.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append(label.description)
    return labels
