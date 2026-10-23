import boto3

from vision_client import load_config, image_bytes_from_payload
from vision_models import normalize_text_blocks


def detect_image_text(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("rekognition", region_name=cfg.get("region"))
    response = client.detect_text(Image={"Bytes": image_bytes_from_payload(payload)})
    return {"text": normalize_text_blocks(response.get("TextDetections", []))}
