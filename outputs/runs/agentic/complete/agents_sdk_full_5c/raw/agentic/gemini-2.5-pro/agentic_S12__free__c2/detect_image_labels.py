import os
import boto3
from vision_models import ImageLabel

def detect_labels(image_bytes: bytes) -> list[ImageLabel]:
    """
    Detects labels in an image using AWS Rekognition.
    """
    rekognition_client = boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_key"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    response = rekognition_client.detect_labels(
        Image={"Bytes": image_bytes}, MaxLabels=10, MinConfidence=75
    )

    labels = []
    for label_data in response.get("Labels", []):
        labels.append(
            ImageLabel(
                name=label_data.get("Name"),
                confidence=label_data.get("Confidence"),
            )
        )
    return labels
