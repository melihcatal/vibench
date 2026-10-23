import boto3
from vision_client import get_rekognition_client
from vision_models import ImagePayload

def score_image_safety(payload: ImagePayload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))
    response = client.detect_moderation_labels(
        Image={"Bytes": payload.image_bytes}
    )

    moderation_labels = [
        {"name": label["ParentName"], "confidence": label["Confidence"] / 100.0}
        for label in response["ModerationLabels"]
    ]
    return {"moderation_labels": moderation_labels}
