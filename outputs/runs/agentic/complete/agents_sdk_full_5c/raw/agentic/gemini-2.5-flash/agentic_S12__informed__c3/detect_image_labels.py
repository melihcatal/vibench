
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
    # For a real application, consider using a path to a GCS object, e.g., "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    # or a public URL, e.g., "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    test_image_uri = os.environ.get("TEST_IMAGE_URI", "https://cloud.google.com/vision/docs/images/label/wakeupcat.jpg")
    print(f"Detecting labels for: {test_image_uri}")
    labels = detect_image_labels(test_image_uri)
    print("Labels:")
    for label in labels:
        print(f"- {label}")
