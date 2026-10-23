
from google.cloud import vision
import os

def describe_image(image_path):
    """Generates a short visual description for an image using Google Cloud Vision API."""

    # Set up Google Cloud credentials
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/keyfile.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description = "This image likely contains: " + ", ".join([label.description for label in labels])
        print(description)
    else:
        print("No visual description could be generated for the image.")

if __name__ == "__main__":
    # Replace with the actual path to your image
    image_to_describe = "path/to/your/image.jpg"
    describe_image(image_to_describe)
