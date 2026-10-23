import os
from typing import Dict, List
import boto3


def check_unsafe_content(text: str) -> Dict:
    """
    Checks extracted document text for unsafe content using Amazon Comprehend.
    """
    client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )

    return {
        "toxicity": response.get("ResultList", [{}])[0].get("Toxicity", 0.0),
        "labels": response.get("ResultList", [{}])[0].get("Labels", []),
    }
