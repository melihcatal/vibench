
import os
from google.cloud import vision

def detect_image_labels(image_content: bytes) -> list:
    """Detects labels in the image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]

if __name__ == '__main__':
    # This is example usage and assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    # Replace with actual image content for testing.
    # For a real application, you might read this from a file or a web request.
    try:
        with open("example.jpg", "rb") as image_file:
            content = image_file.read()
        detected_labels = detect_image_labels(content)
        print("Labels:", detected_labels)
    except FileNotFoundError:
        print("example.jpg not found. Please create an example image file or provide actual image content.")
    except Exception as e:
        print(f"An error occurred: {e}")
