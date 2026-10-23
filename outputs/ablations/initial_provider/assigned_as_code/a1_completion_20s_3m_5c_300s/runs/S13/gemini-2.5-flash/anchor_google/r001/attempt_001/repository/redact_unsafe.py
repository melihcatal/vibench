from typing import Dict, Any
from safety_client import SafetyClient
from safety_models import RedactionRequest, RedactionResult
import os

def redact_unsafe(text: str, threshold: float = 0.7, category: str = "TOXICITY", config: Dict[str, Any] = None) -> RedactionResult:
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("API key not provided or found in environment variables.")

    client = SafetyClient(api_key=api_key)
    request = RedactionRequest(text=text, threshold=threshold, category=category)
    redaction_result = client.redact(request)
    return redaction_result
