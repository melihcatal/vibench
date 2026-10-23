import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def detect_text(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        text = response.text_annotations[0].description if response.text_annotations else 'No text found'
        print('Text:', text)