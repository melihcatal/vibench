from google.cloud import vision_v1
import os

def detect_text(image_path):
    """Detects text in the image using Google Cloud Vision AI."""
    client = vision_v1.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    for text in texts:
        detected_texts.append(text.description)
    
    return detected_texts

