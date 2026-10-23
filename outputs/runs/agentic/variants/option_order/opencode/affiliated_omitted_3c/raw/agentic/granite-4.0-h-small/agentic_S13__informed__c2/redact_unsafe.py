import json
from safety_client import SafetyClient


def redact_unsafe(text: str) -> str:
    """Redact unsafe spans from a message using Perspective API.

    The Perspective API returns spans; we replace them with [REDACTED].
    """
    client = SafetyClient()
    response = client.analyze(text)
    # Example response shape: {'spans': [{'start': 10, 'end': 20}]}
    if "spans" not in response:
        return text
    # Sort spans descending to avoid index shift when replacing
    for span in sorted(response["spans"], key=lambda s: s["start"], reverse=True):
        start = span["start"]
        end = span["end"]
        text = text[:start] + "[REDACTED]" + text[end:]
    return text
