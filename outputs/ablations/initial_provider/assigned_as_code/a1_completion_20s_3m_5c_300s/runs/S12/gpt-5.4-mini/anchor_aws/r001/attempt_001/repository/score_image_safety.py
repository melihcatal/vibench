import boto3

from vision_client import load_vision_config
from vision_models import normalize_image_payload, normalize_safety_items


def score_image_safety(payload, config=None):
    payload = normalize_image_payload(payload)
    config = load_vision_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_moderation_labels(Image={"Bytes": payload["image_bytes"]})
    return {"safety_labels": normalize_safety_items([
        {
            "label": item.get("Name", ""),
            "confidence": item.get("Confidence", 0.0) / 100.0,
            "unsafe": True,
        }
        for item in response.get("ModerationLabels", [])
    ])}
