import boto3

from vision_client import load_vision_config
from vision_models import normalize_image_payload, normalize_text_items


def detect_image_text(payload, config=None):
    payload = normalize_image_payload(payload)
    config = load_vision_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_text(Image={"Bytes": payload["image_bytes"]})
    lines = [item for item in response.get("TextDetections", []) if item.get("Type") == "LINE"]
    return {"text": normalize_text_items([
        {"text": item.get("DetectedText", ""), "confidence": item.get("Confidence", 0.0) / 100.0}
        for item in lines
    ])}
