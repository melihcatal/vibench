# detect_image_labels.py
# [SAME-SCENARIO]

from vision_client import VisionClient
from vision_models import LabelResponse, normalize_labels

# Use AWS Rekognition as the concrete provider
# AWS Rekognition identifies labels/objects in an image


def detect_labels(image_path: str) -> LabelResponse:
    """Detect labels/objects in a static image using AWS Rekognition.

    Returns a normalized LabelResponse containing detected label data.
    """
    client = VisionClient()  # AWS Rekognition client configured internally
    raw_resp = client.detect_labels(
        Image={"S3Object": {"Bucket": "my-bucket", "Name": image_path}}
    )
    return normalize_labels(raw_resp)
