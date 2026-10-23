import os

import boto3


def metric_annotation_safety(text):
    client = boto3.client(
        "comprehend",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    result = client.detect_toxic_text(TextSegments=[{"Text": text}], LanguageCode="en")
    return {
        "provider": "Amazon Comprehend",
        "unsafe": any(
            label.get("Score", 0) >= 0.5 for label in result.get("ResultList", [])
        ),
    }
