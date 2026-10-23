import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = vision.ImageAnnotatorClient()

def detect_text(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')
        for text in texts:
            print(text.description)