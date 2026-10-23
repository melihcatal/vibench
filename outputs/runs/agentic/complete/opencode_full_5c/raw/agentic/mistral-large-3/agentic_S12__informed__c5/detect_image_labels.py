import os
from typing import List, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def detect_labels(
    image_bytes: bytes,
    max_labels: int = 10,
    min_confidence: float = 70.0,
    region: Optional[str] = None,
) -> List[Dict[str, float]]:
    """
    Detects labels in an image using Amazon Rekognition.

    Args:
        image_bytes: Bytes of the image to analyze.
        max_labels: Maximum number of labels to return.
        min_confidence: Minimum confidence score for labels (0-100).
        region: AWS region to use. If None, uses default region.

    Returns:
        List of dictionaries containing 'Label' and 'Confidence' for each detected label.
    """
    if not region:
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    rekognition = boto3.client("rekognition", region_name=region)

    try:
        response = rekognition.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=max_labels,
            MinConfidence=min_confidence,
        )
        return [
            {"Label": label["Name"], "Confidence": label["Confidence"]}
            for label in response["Labels"]
        ]
    except ClientError as e:
        raise Exception(f"Amazon Rekognition error: {e}")
