from safety_client import ComprehendSafetyClient
from typing import Dict, Any

def redact_unsafe(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = ComprehendSafetyClient(region_name=config.get("region", "us-east-1"))

    text = payload["text"]
    language_code = payload.get("language_code", "en")
    threshold = config.get("redaction_threshold", 0.5)

    response = client.redact_unsafe_content(text=text, language_code=language_code, threshold=threshold)

    return {"redacted_text": response.redacted_text, "redaction_spans": [{
        "start": span.start,
        "end": span.end,
        "category": span.category.value,
        "original_text": span.original_text
    } for span in response.spans]}
