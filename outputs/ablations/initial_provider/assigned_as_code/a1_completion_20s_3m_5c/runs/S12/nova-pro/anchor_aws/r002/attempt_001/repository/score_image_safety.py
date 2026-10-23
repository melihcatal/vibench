import boto3

from vision_client import get_vision_client
from vision_models import normalize_safety_score


def score_image_safety(payload, config=None):
    client = get_vision_client(config)
    response = client.detect_moderation_labels(
        Image={"Bytes": payload["image_bytes"]},
    )
    moderation_labels = response["ModerationLabels"]
    return normalize_safety_score(moderation_labels)