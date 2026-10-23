# redact_unsafe.py

import os
from safety_client import TextSafetyClient


def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans from the given text.
    Calls the ibm‑watsonx‑ai Guardrails moderation endpoint and replaces any flagged spans with '[REDACTED]'.
    Returns the cleaned text.
    """
    client = TextSafetyClient()
    result = client.analyze(text=text)
    # Example: assume result contains 'unsafe_spans' list of (start, end) tuples
    spans = result.get("unsafe_spans", [])
    if not spans:
        return text
    # Simple redaction: replace each span with [REDACTED]
    parts = []
    last_end = 0
    for start, end in sorted(spans):
        parts.append(text[last_end:start])
        parts.append("[REDACTED]")
        last_end = end
    parts.append(text[last_end:])
    return "".join(parts)
