# [SAME-SCENARIO] redact_unsafe.py
"""Flags or redacts unsafe spans from text using OpenAI Moderation API."""

import re
from safety_client import get_openai_client


def redact_unsafe(text: str) -> str:
    """Return text with unsafe spans replaced by '[REDACTED]' markers."""
    client = get_openai_client()
    response = client.moderations.create(input=text)
    # response['categories'] contains span info if available (example placeholder)
    unsafe_spans = []
    # Example: extract start/end offsets from response (actual API would provide this)
    for cat in response.get("categories", []):
        if cat.get("flagged"):
            unsafe_spans.append((cat["start"], cat["end"]))
    # Simple redaction using offsets
    parts = []
    last_end = 0
    for start, end in sorted(unsafe_spans):
        parts.append(text[last_end:start])
        parts.append("[REDACTED]")
        last_end = end
    parts.append(text[last_end:])
    return "".join(parts)
