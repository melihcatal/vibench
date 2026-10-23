import re
from typing import List, Dict, Any
from safety_client import ComprehendSafetyClient
from safety_models import TextModerationRequest, RedactionRequest, RedactionResponse

def redact_unsafe(text: str, categories_to_redact: List[str] = None, redaction_character: str = "*", config: Dict[str, Any] = None) -> RedactionResponse:
    config = config or {}
    client = ComprehendSafetyClient(region_name=config.get("region", "us-east-1"))
    
    # First, detect toxic content to determine if redaction is needed.
    moderation_request = TextModerationRequest(text=text, language_code=config.get("language_code", "en"))
    moderation_response = client.detect_toxic_content(moderation_request)

    redacted_text = text
    unsafe_spans = []

    # Simplified redaction: if any of the specified categories exceed a threshold, or if overall toxicity is high,
    # we will redact the entire text for demonstration purposes, as AWS Comprehend toxicity detection doesn't provide spans.
    # In a real-world scenario, you'd use a service that offers span-level detection for specific unsafe content types.
    
    # Example threshold for redaction (can be customized)
    redaction_threshold = config.get("redaction_threshold", 0.7)
    
    should_redact = False
    if categories_to_redact:
        for category in categories_to_redact:
            if moderation_response.toxicity.get(category, {}).get("Score", 0.0) > redaction_threshold:
                should_redact = True
                break
    else:
        # If no specific categories, check overall toxicity
        if moderation_response.toxicity.get("Overall", {}).get("Score", 0.0) > redaction_threshold:
            should_redact = True

    if should_redact:
        # Redact the entire text for simplicity, as span-level toxicity detection is not direct from Comprehend.
        redacted_text = re.sub(r'\S', redaction_character, text) # Redact non-whitespace characters
        unsafe_spans.append({"text": text, "start": 0, "end": len(text), "reason": "Content deemed unsafe by moderation policy"})

    return RedactionResponse(redacted_text=redacted_text, unsafe_spans=unsafe_spans)
