import os
from google.cloud import vision

def detect_labels(image_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        image = vision.Image(content=image_file.read())

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:\n")
    for label in labels:
        print(label.description, "-", label.score)

if __name__ == "__main__":
    detect_labels('path/to/image.jpg')
