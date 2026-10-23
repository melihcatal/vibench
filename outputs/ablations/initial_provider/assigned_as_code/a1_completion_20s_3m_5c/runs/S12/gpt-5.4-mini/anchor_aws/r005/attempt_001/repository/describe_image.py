import boto3

from vision_client import load_config, image_bytes_from_payload
from vision_models import normalize_caption


def describe_image(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("rekognition", region_name=cfg.get("region"))
    response = client.detect_labels(
        Image={"Bytes": image_bytes_from_payload(payload)},
        MaxLabels=1,
    )
    label = response["Labels"][0] if response.get("Labels") else {"Name": "image", "Confidence": 0.0}
    return {"description": normalize_caption(label["Name"], label.get("Confidence", 0.0) / 100.0)}
