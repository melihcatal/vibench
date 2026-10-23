import os
from google.cloud import vision_v1

client = vision_v1.ImageAnnotatorClient()

def check_safety(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision_v1.Image(content=image_file.read())
    response = client.safe_search_detection(image=image)
    return response.safe_search_annotation.adult