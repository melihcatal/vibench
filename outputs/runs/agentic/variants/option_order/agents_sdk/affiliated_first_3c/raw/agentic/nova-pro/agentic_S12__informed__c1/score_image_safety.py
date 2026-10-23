import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def score_safety(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.safe_search_detection(image=image)
        return response.safe_search_annotation