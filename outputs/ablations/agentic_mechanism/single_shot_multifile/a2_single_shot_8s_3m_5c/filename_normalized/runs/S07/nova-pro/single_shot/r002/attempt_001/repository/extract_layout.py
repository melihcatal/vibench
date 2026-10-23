import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def extract_layout(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation