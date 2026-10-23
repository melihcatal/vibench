import boto3

from vision_client import get_vision_client
from vision_models import normalize_text


def detect_image_text(payload, config=None):
    client = get_vision_client(config)
    response = client.detect_text(
        Image={"Bytes": payload["image_bytes"]},
    )
    text_detections = response["TextDetections"]
    return [normalize_text(detection["DetectedText"]) for detection in text_detections]