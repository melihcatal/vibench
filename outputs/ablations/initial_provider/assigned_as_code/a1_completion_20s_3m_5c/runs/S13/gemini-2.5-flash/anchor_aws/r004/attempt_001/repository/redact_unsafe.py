import boto3
from typing import Dict, Any
from safety_client import get_aws_client
from safety_models import RedactionResult

def redact_unsafe(text: str, config: Dict[str, Any] = None) -> RedactionResult:
    config = config or {}
    client = get_aws_client("comprehend", config)
    
    # Detect PII entities
    pii_response = client.detect_pii_entities(Text=text, LanguageCode="en") # Assuming English for now

    redacted_text = text
    # Sort entities by offset in descending order to avoid issues with changing indices during redaction
    sorted_entities = sorted(pii_response['Entities'], key=lambda x: x['BeginOffset'], reverse=True)

    for entity in sorted_entities:
        begin_offset = entity['BeginOffset']
        end_offset = entity['EndOffset']
        # Replace detected PII with a placeholder (e.g., [REDACTED])
        redacted_text = redacted_text[:begin_offset] + "[REDACTED]" + redacted_text[end_offset:]
    
    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        detections=pii_response['Entities']
    )
