import os
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()


def detect_labels(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print("Labels:")
    for label in labels:
        print(label.description)


if __name__ == "__main__":
    detect_labels("path_to_image.jpg")
