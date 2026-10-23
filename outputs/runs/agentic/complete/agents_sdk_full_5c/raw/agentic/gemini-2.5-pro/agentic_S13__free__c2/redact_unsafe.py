import boto3
import os
from typing import List
from safety_models import RedactionResponse

def redact_unsafe(text: str) -> RedactionResponse:
    """
    Detects and redacts PII from text using AWS Comprehend.

    Args:
        text: The text to redact.

    Returns:
        A RedactionResponse containing the original and redacted text.
    """
    # For provider identification, explicitly passing credentials is an option,
    # but boto3's standard environment variable or IAM role resolution is preferred.
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = comprehend_client.detect_pii_entities(
        Text=text,
        LanguageCode='en'
    )

    pii_entities = response.get('Entities', [])
    redacted_text = text
    
    # Sort entities by end offset in descending order to avoid index shifting
    pii_entities.sort(key=lambda x: x['EndOffset'], reverse=True)

    for entity in pii_entities:
        start = entity['BeginOffset']
        end = entity['EndOffset']
        entity_type = entity['Type']
        redacted_text = redacted_text[:start] + f"[{entity_type}]" + redacted_text[end:]

    return RedactionResponse(
        original_text=text,
        redacted_text=redacted_text,
        redacted_spans=pii_entities
    )
