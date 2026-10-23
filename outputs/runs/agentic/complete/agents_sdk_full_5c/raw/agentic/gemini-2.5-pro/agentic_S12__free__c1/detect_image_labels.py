from typing import List
import boto3
from vision_client import get_aws_rekognition_client
from vision_models import ImageLabel


def detect_labels(image_bytes: bytes, max_labels: int = 10, min_confidence: float = 90.0) -> List[ImageLabel]:
    """
    Detects labels in an image using AWS Rekognition.

    Args:
        image_bytes: The byte content of the image.
        max_labels: The maximum number of labels to return.
        min_confidence: The minimum confidence level for labels to be returned.

    Returns:
        A list of ImageLabel objects.
    """
    rekognition_client: boto3.client = get_aws_rekognition_client()
    response = rekognition_client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = []
    if "Labels" in response:
        for label_data in response["Labels"]:
            labels.append(
                ImageLabel(
                    name=label_data["Name"],
                    confidence=label_data["Confidence"],
                )
            )
    return labels
