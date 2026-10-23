from typing import List, Optional
import os

import boto3
from vision_models import ImageLabel, VisualAnalysis


def detect_labels(image_uri: str, max_labels: int = 10, min_confidence: float = 90.0) -> List[ImageLabel]:
    """
    Detects labels in an image using AWS Rekognition.

    Args:
        image_uri: S3 URI of the image (e.g., "s3://bucket/key").
        max_labels: The maximum number of labels to return.
        min_confidence: The minimum confidence level for the labels to return.

    Returns:
        A list of ImageLabel objects.
    """
    if not image_uri.startswith("s3://"):
        raise ValueError("Image URI must be an S3 URI (s3://bucket/key)")

    bucket, key = image_uri.replace("s3://", "").split("/", 1)

    rekognition_client = boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = rekognition_client.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = []
    if "Labels" in response:
        for label_data in response["Labels"]:
            labels.append(
                ImageLabel(
                    label=label_data["Name"],
                    confidence=label_data["Confidence"] / 100.0,
                    provider="aws_rekognition",
                )
            )
    return labels

def detect_image_labels(analysis: VisualAnalysis) -> VisualAnalysis:
    """Detects labels and adds them to the analysis object."""
    if not analysis.source_uri:
        raise ValueError("Analysis object must have a source_uri")

    labels = detect_labels(image_uri=analysis.source_uri)
    analysis.labels = labels
    return analysis
