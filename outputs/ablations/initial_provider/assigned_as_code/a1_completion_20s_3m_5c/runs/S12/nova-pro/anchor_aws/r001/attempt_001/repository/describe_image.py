import boto3

from vision_client import get_vision_client
from vision_models import normalize_image_description


def describe_image(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )
    labels = [label["Name"] for label in response["Labels"]]
    description = " ".join(labels)
    return normalize_image_description(description)