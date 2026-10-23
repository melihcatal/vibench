import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def detect_labels(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        return response.label_annotations