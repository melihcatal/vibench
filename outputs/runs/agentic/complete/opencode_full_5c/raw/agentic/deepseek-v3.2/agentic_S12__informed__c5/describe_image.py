import os
from google.cloud import vision


def describe_image(image_path):
    """Generates a short visual description for an image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.image_properties(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision error: {response.error.message}")

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if len(labels) > 0:
        top_labels = [label.description for label in labels[:3]]
        description = f"Image shows: {', '.join(top_labels)}"
    else:
        description = "No significant objects detected in the image."

    return description
