import boto3

from vision_client import load_vision_config
from vision_models import normalize_image_payload


def describe_image(payload, config=None):
    payload = normalize_image_payload(payload)
    config = load_vision_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=1,
        MinConfidence=50.0,
    )
    labels = response.get("Labels", [])
    if not labels:
        return {"description": ""}
    label = labels[0]["Name"]
    return {"description": f"An image showing {label.lower()}."}
