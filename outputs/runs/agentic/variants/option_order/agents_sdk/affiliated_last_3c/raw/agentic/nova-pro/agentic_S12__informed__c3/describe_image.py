import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = vision.ImageAnnotatorClient()

def describe_image(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = response.label_annotations
        description = ' '.join([label.description for label in labels])
        return description