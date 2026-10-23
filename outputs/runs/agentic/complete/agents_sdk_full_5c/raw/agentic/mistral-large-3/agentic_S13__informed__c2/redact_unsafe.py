"""
Flag or redact unsafe spans from text using Azure AI Content Safety.
"""
from typing import Dict, List, Optional

from safety_client import AzureContentSafetyClient
from safety_models import SafetyRequest, SafetyResponse


client = AzureContentSafetyClient()


def redact_unsafe(text: str, categories: Optional[List[str]] = None, redact_char: str = "*") -> Dict:
    """Redact unsafe spans from text."""
    request: SafetyRequest = {
        "text": text,
        "categories": categories,
        "threshold": None
    }
    response: SafetyResponse = client.moderate(request)
    
    # Simulate redaction based on flagged categories
    redacted_text = text
    for category in response["categories"]:
        if category["label"] == "flagged":
            redacted_text = redacted_text.replace(text, redact_char * len(text))
            break
    
    return {
        "original_text": response["text"],
        "redacted_text": redacted_text,
        "flagged": response["flagged"],
        "categories": [
            {
                "category": c["category"],
                "score": c["score"],
                "label": c["label"]
            }
            for c in response["categories"]
        ],
        "provider": response["provider"]
    }