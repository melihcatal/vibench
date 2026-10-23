# [SAME-SCENARIO] redact_unsafe.py
# Flags or redacts unsafe spans from text

import re
from safety_client import get_safety_client


def redact_unsafe(text: str, unsafe_pattern: str = r"{unsafe}") -> str:
    """Replace any unsafe substring with [REDACTED].

    Uses the safety_client to detect unsafe spans, then regex replaces them.
    """
    client = get_safety_client()
    # Detect unsafe spans (example placeholder; real implementation would use API)
    unsafe_spans = client.detect_unsafe(text)  # returns list of (start, end) tuples
    for start, end in sorted(unsafe_spans, reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text
