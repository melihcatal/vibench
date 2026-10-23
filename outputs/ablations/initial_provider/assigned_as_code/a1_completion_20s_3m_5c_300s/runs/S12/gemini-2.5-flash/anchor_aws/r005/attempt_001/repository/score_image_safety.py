from vision_client import get_rekognition_client
from vision_models import normalize_moderation_labels


def score_image_safety(payload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))
    response = client.detect_moderation_labels(
        Image={"Bytes": payload["image_bytes"]}
    )
    return {"moderation_labels": normalize_moderation_labels(response)}
