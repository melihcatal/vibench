import os
from typing import List
import boto3
from vision_models import LabelDetectionResponse


def check_visual_labels_safety(labels: LabelDetectionResponse) -> bool:
    """Check generated visual labels for unsafe text using Amazon Comprehend."""
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    text_list = labels.labels
    if not text_list:
        return True

    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": label} for label in text_list]
    )

    for result in response.get("ResultList", []):
        for toxicity_score in result.get("ToxicityScores", []):
            if toxicity_score > 0.5:
                return False

    return True