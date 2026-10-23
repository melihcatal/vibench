import boto3

from vision_client import get_vision_client
from vision_models import normalize_image_summary


def image_summary(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    labels = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )["Labels"]
    text = client.detect_text(
        Image={"Bytes": payload["image_bytes"]},
    )["TextDetections"]
    summary = " ".join([label["Name"] for label in labels] + [detection["DetectedText"] for detection in text])
    return normalize_image_summary(summary)