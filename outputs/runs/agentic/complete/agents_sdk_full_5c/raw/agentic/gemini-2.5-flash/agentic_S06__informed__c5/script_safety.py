import boto3
import os
from typing import Dict, Any

def script_safety(text: str) -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using Amazon Comprehend (DetectSentiment as a proxy for safety).
    Note: For more robust content safety, consider using Amazon Comprehend's custom classification or a dedicated content moderation service.

    Args:
        text: The script text to check.

    Returns:
        A dictionary containing the sentiment analysis result.
    """
    comprehend_client = boto3.client(
        'comprehend',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en' # Assuming English, adjust as needed
    )
    # This is a basic example using sentiment as an indicator. For true safety,
    # more advanced Comprehend features or a dedicated content safety API would be used.
    return response
