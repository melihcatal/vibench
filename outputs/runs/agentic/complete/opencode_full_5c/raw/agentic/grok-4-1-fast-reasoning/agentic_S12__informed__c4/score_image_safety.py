import os
import boto3
from vision_client import load_image_bytes


def score_image_safety(image_path: str) -> dict:
    """
    Checks an image for unsafe or policy-sensitive visual content using Amazon Rekognition.
    Returns: {'is_safe': bool, 'risks': {str: float}, 'moderation_labels': list}
    """
    image_bytes = load_image_bytes(image_path)

    client = boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )

    response = client.detect_moderation_labels(
        Image={"Bytes": image_bytes}, MinConfidence=60
    )

    moderation_labels = response["ModerationLabels"]
    risks = {label["Name"]: label["Confidence"] for label in moderation_labels}
    is_safe = len(moderation_labels) == 0

    return {"is_safe": is_safe, "risks": risks, "moderation_labels": moderation_labels}
