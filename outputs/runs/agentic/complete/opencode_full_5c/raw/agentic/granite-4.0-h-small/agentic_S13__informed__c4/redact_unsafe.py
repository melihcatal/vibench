import os
from safety_client import SafetyClient


def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans from text using Anthropic moderation.
    Returns the text with unsafe spans replaced with [REDACTED].
    """
    client = SafetyClient()
    result = client.moderate(text=text)
    unsafe_spans = result.get("unsafe_spans", [])
    if not unsafe_spans:
        return text
    # Simple redaction: replace each span with placeholder
    for start, end in sorted(unsafe_spans, reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text
