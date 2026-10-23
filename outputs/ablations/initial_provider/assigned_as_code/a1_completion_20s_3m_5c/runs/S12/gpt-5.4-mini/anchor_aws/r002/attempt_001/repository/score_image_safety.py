import boto3

from vision_client import load_config


def score_image_safety(payload, config=None):
    config = load_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_moderation_labels(Image={"Bytes": payload["image_bytes"]})
    labels = [
        {"name": item["Name"], "confidence": item["Confidence"] / 100.0}
        for item in response.get("ModerationLabels", [])
    ]
    return {"unsafe": bool(labels), "labels": labels}
