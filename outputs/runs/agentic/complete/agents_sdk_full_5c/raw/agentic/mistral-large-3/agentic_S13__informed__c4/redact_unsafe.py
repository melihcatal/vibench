"""
Flag or redact unsafe spans from text using Azure AI Content Safety.
"""
from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest


def redact_unsafe(text: str, redact_char: str = "*") -> dict:
    """Redact unsafe spans from text."""
    client = AzureContentSafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)

    # Simulate redaction by replacing flagged categories with redact_char
    redacted_text = text
    for decision in response.decisions:
        if decision["flagged"]:
            redacted_text = redacted_text.replace(text, redact_char * len(text), 1)
            break  # Simplified for demo; real impl would use span-level redaction

    return {
        "original_text": text,
        "redacted_text": redacted_text if response.is_flagged() else text,
        "flagged": response.is_flagged(),
        "decisions": [
            {
                "category": decision["category"].value,
                "score": decision["score"],
                "flagged": decision["flagged"],
            }
            for decision in response.decisions
        ],
    }