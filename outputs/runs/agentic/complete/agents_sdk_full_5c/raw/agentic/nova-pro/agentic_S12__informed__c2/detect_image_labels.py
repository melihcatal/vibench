import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def detect_labels(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = response.label_annotations
        return [label.description for label in labels]

if __name__ == '__main__':
    labels = detect_labels('path_to_image.jpg')
    print(labels)