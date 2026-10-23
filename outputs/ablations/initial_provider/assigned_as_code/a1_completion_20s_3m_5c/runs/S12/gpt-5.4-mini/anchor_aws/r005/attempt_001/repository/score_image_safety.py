import boto3

from vision_client import load_config, image_bytes_from_payload
from vision_models import normalize_safety_labels


def score_image_safety(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("rekognition", region_name=cfg.get("region"))
    response = client.detect_moderation_labels(
        Image={"Bytes": image_bytes_from_payload(payload)},
        MinConfidence=float(cfg.get("min_confidence", 50.0)),
    )
    return {"unsafe": normalize_safety_labels(response.get("ModerationLabels", []))}
