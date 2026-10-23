import os
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()


def detect_text(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    text_annotations = response.text_annotations
    print("Text in the image:")
    for annotation in text_annotations:
        print(annotation.description)


if __name__ == "__main__":
    detect_text("path_to_image.jpg")
