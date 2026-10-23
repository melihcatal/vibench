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
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # For demonstration, replace with a public image URI or GCS URI.
    # For a real application, handle image content bytes directly.
    # print(detect_image_labels("gs://cloud-samples-data/vision/label/wakeupcat.jpg"))
    pass
