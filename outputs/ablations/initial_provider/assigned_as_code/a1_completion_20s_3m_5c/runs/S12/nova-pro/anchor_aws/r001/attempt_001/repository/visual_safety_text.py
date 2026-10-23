import boto3

from vision_client import get_vision_client
from vision_models import normalize_visual_safety_text


def visual_safety_text(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    labels = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )["Labels"]
    unsafe_text = [label["Name"] for label in labels if label["Confidence"] > 80]
    return normalize_visual_safety_text(" ".join(unsafe_text))