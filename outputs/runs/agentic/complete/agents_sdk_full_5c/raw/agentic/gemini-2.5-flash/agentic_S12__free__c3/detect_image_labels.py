from google.cloud import vision
import os

def detect_labels(image_uri: str) -> list[str]:
    """Detects labels in the image at the given Google Cloud Storage URI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # This is a placeholder for actual usage.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or configure authentication.
    # Example image from Google Cloud Public Dataset
    # gs://cloud-samples-data/vision/label/wakeupcat.jpg
    image_uri = os.environ.get("IMAGE_URI", "gs://cloud-samples-data/vision/label/wakeupcat.jpg")
    print(f"Detecting labels for image: {image_uri}")
    detected_labels = detect_labels(image_uri)
    print("Labels:")
    for label in detected_labels:
        print(f"- {label}")
