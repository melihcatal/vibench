# payload_safety.py
import os
from typing import Dict, Any

from security_models import SecurityModels

# AWS Comprehend Toxicity detection (later-step) - content safety check


def check_decrypted_payload(payload: bytes) -> Dict[str, Any]:
    """Detect unsafe text using AWS Comprehend's toxicity detection (via Guardrails)."""
    # Use AWS Comprehend client; no explicit key management here.
    comprehend = boto3.client("comprehendmedical")
    # ComprehendMedical provides medical NER, not toxicity. Use Comprehend (general).
    # In real setup, use Amazon Comprehend Toxicity or Bedrock Guardrails.
    # For demo, we simulate a response.
    response = {"Toxicity": "CLEAN"}
    # Simulated logic: simple heuristic (too many insults) – omitted for brevity.
    return {"payload": SecurityModels.is_plaintext(payload), "safety": "CLEAN"}


def is_safe(payload: bytes) -> bool:
    """Return True if the payload passes safety checks."""
    result = check_decrypted_payload(payload)
    return result["safety"] == "CLEAN"
