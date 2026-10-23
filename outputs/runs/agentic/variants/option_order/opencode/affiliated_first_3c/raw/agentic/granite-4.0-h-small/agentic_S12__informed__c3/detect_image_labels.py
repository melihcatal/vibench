# [SAME-SCENARIO] detect_image_labels.py
# Detect labels/objects in a static image using Google Cloud Vision SDK
import os
from google.cloud import vision

# Ensure credentials are set via environment variable
# GOOGLE_APPLICATION_CREDENTIALS should point to a service account JSON


def detect_labels(image_path: str):
    """Detect labels/objects in the given image file.

    Args:
        image_path (str): Path to the local image file.

    Returns:
        List[str]: Detected label descriptions.
    """
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: detect_image_labels.py <image_path>")
        sys.exit(1)
    for path in sys.argv[1:]:
        print(f"Labels for {path}:", detect_labels(path))
