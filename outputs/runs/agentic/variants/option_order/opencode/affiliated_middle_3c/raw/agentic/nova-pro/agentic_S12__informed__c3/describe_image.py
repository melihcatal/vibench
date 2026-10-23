import os
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()


def describe_image(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    description = " ".join([label.description for label in labels])
    print("Image Description:", description)


if __name__ == "__main__":
    describe_image("path_to_image.jpg")
