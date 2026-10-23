import boto3
import os
from typing import Dict, Any

def script_safety(text: str) -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using AWS Comprehend.
    """
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode="en"
    )

    # For a more comprehensive safety check, one might use other Comprehend APIs like detect_dominant_language,
    # detect_pii_entities, or custom classification models. Here, we're using sentiment for a basic check.
    return response
