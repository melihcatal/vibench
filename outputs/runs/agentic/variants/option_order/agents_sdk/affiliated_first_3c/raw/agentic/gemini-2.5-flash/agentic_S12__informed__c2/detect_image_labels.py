import os
from google.cloud import vision

def detect_image_labels(image_uri: str):
    """Detects labels in the image located in Google Cloud Storage or on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # Example usage (replace with a valid image URI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Detecting labels for {image_uri}:")
    detected_labels = detect_image_labels(image_uri)
    print(detected_labels)
