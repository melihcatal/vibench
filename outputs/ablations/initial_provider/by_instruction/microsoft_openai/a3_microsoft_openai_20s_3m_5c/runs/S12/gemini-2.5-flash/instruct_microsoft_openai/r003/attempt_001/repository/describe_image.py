import os
from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description = ", ".join([label.description for label in labels])
        return f"The image likely contains: {description}."
    else:
        return "No clear description could be generated for the image."
