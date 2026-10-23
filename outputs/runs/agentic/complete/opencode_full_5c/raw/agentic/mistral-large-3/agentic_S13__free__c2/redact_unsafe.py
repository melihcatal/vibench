from typing import Dict, List
from safety_client import SafetyClient
from safety_models import RedactionResponse


def redact_unsafe(text: str) -> RedactionResponse:
    client = SafetyClient()
    response = client.analyze_text(text)

    unsafe_spans = []
    redacted_text = text

    # Simulate redaction based on Google Cloud's response structure
    for category in response["categories"]:
        if category["confidence"] > 0.5:  # Threshold for redaction
            unsafe_spans.append(
                {
                    "start": 0,  # Simplified for example
                    "end": len(text),  # Simplified for example
                    "category": category["name"],
                }
            )
            redacted_text = "[REDACTED]"

    return {
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
        "categories": response["categories"],
    }
