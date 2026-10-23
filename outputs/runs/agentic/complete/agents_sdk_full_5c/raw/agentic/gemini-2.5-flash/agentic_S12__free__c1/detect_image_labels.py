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
    # Example usage with a public image
    # GOOGLE_APPLICATION_CREDENTIALS must be set for local execution
    # For demonstration, a placeholder image URI is used.
    # In a real scenario, this would come from a user or another service.
    example_image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Detecting labels for: {example_image_uri}")
    detected_labels = detect_image_labels(example_image_uri)
    print(f"Labels: {detected_labels}")
