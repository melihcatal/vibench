import boto3

from vision_client import load_config


def describe_image(payload, config=None):
    config = load_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_labels(Image={"Bytes": payload["image_bytes"]}, MaxLabels=5)
    labels = [label["Name"] for label in response.get("Labels", [])[:3]]
    return {"description": ", ".join(labels)}
