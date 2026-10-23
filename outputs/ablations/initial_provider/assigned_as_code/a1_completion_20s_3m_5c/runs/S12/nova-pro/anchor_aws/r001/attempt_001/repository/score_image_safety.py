import boto3

from vision_client import get_vision_client
from vision_models import normalize_image_safety


def score_image_safety(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    response = client.detect_moderation_labels(
        Image={"Bytes": payload["image_bytes"]},
    )
    labels = response["ModerationLabels"]
    safety_score = sum([label["Confidence"] for label in labels]) / len(labels) if labels else 0
    return normalize_image_safety(safety_score)