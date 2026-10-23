
from google.cloud import vision
import os

def detect_labels(image_path):
    # Set up Google Cloud credentials (if not already set via GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/key.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print(f"Labels for image: {image_path}")
    for label in labels:
        print(f"  {label.description} (score: {label.score:.2f})")

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    image_file = 'path/to/your/image.jpg'
    detect_labels(image_file)
