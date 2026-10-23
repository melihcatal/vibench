from google.cloud import vision
import os

def detect_labels(image_path):
    """Detects labels in the image at the given file path."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(f'{label.description} (score: {label.score:.2f})')

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your image
    # and ensure you have authenticated with Google Cloud (e.g., via GOOGLE_APPLICATION_CREDENTIALS)
    detect_labels('path/to/your/image.jpg')
