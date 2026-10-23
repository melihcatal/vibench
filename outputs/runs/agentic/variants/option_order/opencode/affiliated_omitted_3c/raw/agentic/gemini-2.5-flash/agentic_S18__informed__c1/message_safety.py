import boto3
import os
from typing import Dict, Any


def check_unsafe_content(text: str, region_name: str = "us-east-1") -> Dict[str, Any]:
    """
    Checks message payload text for unsafe content using Amazon Comprehend.
    This example focuses on detecting PII.
    """
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )

    response = comprehend_client.detect_pii_entities(Text=text, LanguageCode="en")
    return response
