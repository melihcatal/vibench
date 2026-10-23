import boto3
import os
from vision_client import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    load_image_bytes,
)


def score_image_safety(image_path: str) -> dict:
    client = boto3.client(
        "rekognition",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    image_bytes = load_image_bytes(image_path)
    response = client.detect_moderation_labels(Image={"Bytes": image_bytes})
    violations = [
        label["Name"]
        for label in response["ModerationLabels"]
        if label["Confidence"] > 60.0
    ]
    safe = len(violations) == 0
    return {"safe": safe, "violations": violations}
