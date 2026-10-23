import boto3

from vision_client import load_config


def detect_image_text(payload, config=None):
    config = load_config(config)
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_text(Image={"Bytes": payload["image_bytes"]})
    lines = [item["DetectedText"] for item in response.get("TextDetections", []) if item.get("Type") == "LINE"]
    return {"text": lines}
