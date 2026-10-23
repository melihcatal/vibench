import boto3
from typing import Dict, Any, List
from safety_client import get_comprehend_client

def redact_unsafe(text: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_comprehend_client(config.get("region", "us-east-1"))
    
    # Detect PII entities
    pii_response = client.detect_pii_entities(
        Text=text,
        LanguageCode="en"
    )
    
    # Redact PII entities. Comprehend doesn't have a direct 'redact_text' for general unsafe content,
    # but it does for PII. For other unsafe content, a custom redaction logic would be needed
    # based on the detect_toxic_content output. For this example, we focus on PII redaction.
    
    redacted_text = text
    # Sort entities by offset in reverse to avoid issues with changing indices during redaction
    sorted_entities = sorted(pii_response["Entities"], key=lambda x: x["BeginOffset"], reverse=True)
    
    for entity in sorted_entities:
        begin = entity["BeginOffset"]
        end = entity["EndOffset"]
        # Replace with asterisks for redaction
        redacted_text = redacted_text[:begin] + "*" * (end - begin) + redacted_text[end:]
        
    # Also detect toxic content for flagging purposes, even if not directly redacted by Comprehend's redact_pii
    toxicity_response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
    toxicity_score = toxicity_response["ResultList"][0]["Toxicity"]
    
    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "pii_entities": pii_response["Entities"],
        "toxicity_score": toxicity_score,
        "is_potentially_unsafe": toxicity_score > config.get("redaction_toxicity_threshold", 0.5) # Example threshold
    }
