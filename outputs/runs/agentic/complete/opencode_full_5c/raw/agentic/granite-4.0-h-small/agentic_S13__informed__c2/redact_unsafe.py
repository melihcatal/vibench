# [SAME-SCENARIO] redact_unsafe.py
"""Flag or redact unsafe spans from user text based on moderation results.
Demonstrates a local helper that can replace prohibited substrings with [REDACTED].
"""

import re
from safety_client import get_content_moderation_client


def redact_unsafe(text: str):
    """Return text with unsafe spans replaced by [REDACTED]."""
    client = get_content_moderation_client()
    # Assume the client returns a list of unsafe spans: [{"start": int, "end": int}]
    unsafe_spans = client.detect_unsafe_spans(text)
    # Sort spans by start descending to avoid shifting indices
    for span in sorted(unsafe_spans, key=lambda s: s["start"], reverse=True):
        start, end = span["start"], span["end"]
        text = text[:start] + "[REDACTED]" + text[end:]
    return text
