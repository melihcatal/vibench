import requests
from google.cloud import vision
from typing import List
from vision_models import ImageLabel

def detect_labels_in_image(image_uri: str) -> List[ImageLabel]:
    """
    Detects labels in an image using Google Cloud Vision API.
    The image can be a remote URL or a local file path.
    """
    client = vision.ImageAnnotatorClient()

    # Check if the image_uri is a remote URL
    if image_uri.startswith('http://') or image_uri.startswith('https://'):
        response = requests.get(image_uri, stream=True)
        response.raise_for_status()
        content = response.content
        image = vision.Image(content=content)
    else:
        # Assume it's a local file path
        with open(image_uri, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    detected_labels = [
        ImageLabel(label=label.description, score=label.score)
        for label in labels
    ]
    
    return detected_labels
