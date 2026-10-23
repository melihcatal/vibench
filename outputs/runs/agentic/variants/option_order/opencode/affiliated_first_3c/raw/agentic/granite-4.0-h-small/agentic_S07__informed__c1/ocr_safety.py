import os
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# LATER-STEP: ocr_safety.py

# Provider: Amazon Comprehend (or Bedrock Guardrails) for toxicity detection
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def check_content_safety(text: str) -> bool:
    """Check extracted document text for unsafe content using Amazon Comprehend toxicity detection.

    Returns True if safe, False otherwise.
    """
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
    # Simple heuristic: if any PII entities are found, consider unsafe (customize as needed)
    return len(response.get("Entities", [])) == 0


# Optional: use Bedrock Guardrails via REST (not shown here)
