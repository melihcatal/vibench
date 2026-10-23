import os
from google.cloud import vision

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')
        for text in texts:
            print(text.description)