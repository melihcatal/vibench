import os
import boto3
from typing import List
from identity_models import ModerationResult

def moderate_text_with_aws_comprehend(text: str) -> ModerationResult:
    """Moderates free-text claims or notes using AWS Comprehend for PII detection and sentiment analysis."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "YOUR_AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "YOUR_AWS_SECRET_ACCESS_KEY")

    comprehend = boto3.client(
        "comprehend",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    is_flagged = False
    reasons: List[str] = []
    moderated_text = text

    try:
        # Detect PII entities
        pii_response = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
        if pii_response["Entities"]:
            is_flagged = True
            reasons.append("PII detected")
            # In a real scenario, you might redact PII. For this example, we just flag it.
            # For simplicity, we are not redacting here, but you would iterate through entities
            # and replace them with '[REDACTED]' or similar.

        # Detect sentiment
        sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
        if sentiment_response["Sentiment"] in ["NEGATIVE", "MIXED"]:
            is_flagged = True
            reasons.append(f"Sentiment: {sentiment_response['Sentiment']}")
            
        # Detect inappropriate content (custom classification not directly available through simple Comprehend APIs)
        # For advanced content moderation, AWS Rekognition for images or custom ML models might be needed.
        # For text, we are relying on PII and sentiment as indicators for now.

    except Exception as e:
        reasons.append(f"Error during moderation: {str(e)}")
        # Depending on the error, you might want to flag it as well.
        is_flagged = True

    return ModerationResult(
        original_text=text,
        moderated_text=moderated_text,
        is_flagged=is_flagged,
        reasons=reasons
    )

def claims_moderation(claim_text: str) -> ModerationResult:
    """Entry point for moderating free-text claims."""
    return moderate_text_with_aws_comprehend(claim_text)
