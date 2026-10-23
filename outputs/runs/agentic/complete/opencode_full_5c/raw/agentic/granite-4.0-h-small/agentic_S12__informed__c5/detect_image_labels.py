import json
from vision_client import VisionClient  # uses Amazon Rekognition via boto3


def detect_image_labels(image_path: str) -> list:
    """Detects labels (objects) in a static image using Amazon Rekognition.

    Returns a list of detected label names.
    """
    client = VisionClient()  # Rekognition client via boto3
    response = client.detect_labels(Image={"Bytes": client.read_image(image_path)})
    # Normalize and return label names
    labels = [label["Name"] for label in response.get("Labels", [])]
    return labels
