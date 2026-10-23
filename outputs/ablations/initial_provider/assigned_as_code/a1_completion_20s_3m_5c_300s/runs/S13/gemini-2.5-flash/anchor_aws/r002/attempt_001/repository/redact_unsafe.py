import boto3
from typing import Dict, Any
from safety_client import get_aws_client
from safety_models import RedactionResult

def redact_unsafe(payload: Dict[str, Any], config: Dict[str, Any] = None) -> RedactionResult:
    config = config or {}
    client = get_aws_client("comprehend", region_name=config.get("region", "us-east-1"))
    
    text = payload["text"]
    language_code = payload.get("language_code", "en")

    # Detect PII entities
    pii_response = client.detect_pii_entities(Text=text, LanguageCode=language_code)
    entities = pii_response["Entities"]

    # Redact PII entities. Comprehend doesn't have a direct redact API for general text.
    # So we'll manually replace detected PII entities with a placeholder.
    redacted_text = list(text) # Convert to list to allow modification
    detections = []

    # Sort entities by begin offset in descending order to avoid index issues during redaction
    sorted_entities = sorted(entities, key=lambda x: x['BeginOffset'], reverse=True)

    for entity in sorted_entities:
        begin = entity["BeginOffset"]
        end = entity["EndOffset"]
        entity_type = entity["Type"]
        
        # Replace with asterisks for redaction
        redacted_text[begin:end] = ['*' * (end - begin)]
        
        detections.append({
            "type": entity_type,
            "begin_offset": begin,
            "end_offset": end,
            "score": entity["Score"]
        })

    return RedactionResult(
        original_text=text,
        redacted_text="".join(redacted_text),
        detections=detections
    )
