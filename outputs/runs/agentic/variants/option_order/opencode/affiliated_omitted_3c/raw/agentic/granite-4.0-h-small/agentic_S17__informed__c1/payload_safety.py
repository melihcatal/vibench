import os
import json
import base64
from typing import Any, Dict

# Example: use Amazon Comprehend Toxicity detection via Boto3
import boto3

# Configure AWS client using env vars (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
safety_client = boto3.client("comprehend")

# Configuration (region can be set via env var AWS_DEFAULT_REGION)
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def is_payload_safe(text: str) -> bool:
    """Check a decrypted text payload for unsafe content using AWS Comprehend Toxicity detection.

    Returns True if safe, False otherwise.
    """
    response = safety_client.detect_sentiment(Text=text, LanguageCode="en")
    # Simplified: treat any sentiment other than POSITIVE as unsafe (placeholder)
    sentiment = response.get("Sentiment")
    return sentiment == "POSITIVE"


# Example: alternate perspective API implementation (kept commented)
# perspective_client = ...   # initialize with PERSPECTIVE_API_KEY
# def is_payload_safe(text: str) -> bool:
#     result = perspective_client.analyze_comment(content=text, languages=["en"])
#     return result['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5
