from google.cloud import vision
import os

def detect_image_labels(image_uri: str):
    """Detects labels in the image."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # This is an example, replace with a real image URI
    # For authentication, set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    labels = detect_image_labels(image_uri)
    print(f"Labels for {image_uri}: {labels}")
