import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def detect_text(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return [text.description for text in texts]

if __name__ == '__main__':
    texts = detect_text('path_to_image.jpg')
    print(texts)