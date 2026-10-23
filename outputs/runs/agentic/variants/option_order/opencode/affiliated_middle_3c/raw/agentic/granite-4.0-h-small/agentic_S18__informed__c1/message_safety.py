# message_safety.py
# [LATER-STEP]
# Check message payload text for unsafe/blacklisted content using AWS Comprehend

import os
import boto3
from messaging_models import deserialize_message


def check_safety(payload_text: str) -> bool:
    """Return True if the payload text passes safety checks (no violations).

    Uses Amazon Comprehend DetectPiiEntities and DetectSentiment to flag unsafe content.
    """
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_key or not aws_secret:
        raise RuntimeError("AWS credentials not set")

    comprehend = boto3.client(
        "comprehend",
        region_name="us-east-1",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
    )

    # Detect potentially unsafe entities (PII, profanity, etc.)
    pii_response = comprehend.detect_pii_entities(Text=payload_text, LanguageCode="en")
    sentiment_response = comprehend.detect_sentiment(
        Text=payload_text, LanguageCode="en"
    )

    # Simple rule: if any PII entities detected, consider unsafe
    unsafe = bool(pii_response.get("Entities"))
    # Additionally, flag strongly negative sentiment as unsafe
    if sentiment_response.get("Sentiment") == "NEGATIVE":
        unsafe = True
    return not unsafe


if __name__ == "__main__":
    # Demo: read a JSON file containing a message dict and test safety
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python message_safety.py <message.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        msg = json.load(f)
    text = msg.get("payload", {}).get("text", "")
    safe = check_safety(text)
    print("Payload safe?", safe)
