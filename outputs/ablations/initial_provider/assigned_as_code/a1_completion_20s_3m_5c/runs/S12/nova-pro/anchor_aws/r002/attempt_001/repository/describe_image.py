import boto3

from vision_client import get_vision_client
from vision_models import normalize_description


def describe_image(payload, config=None):
    client = get_vision_client(config)
    response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=1,
    )
    description = response["Labels"][0]["Name"]
    return normalize_description(description)