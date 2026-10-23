import re
from safety_client import SafetyClient

# Example: using Perspective API – provider flagged in client
CLIENT = SafetyClient()


def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans from text.

    Uses the provider's unsafe span detection and replaces those spans with '[REDACTED]'.
    Returns the cleaned text.
    """
    unsafe_spans = CLIENT.detect_unsafe_spans(text)
    # unsafe_spans is a list of (start, end) tuples
    parts = []
    last_idx = 0
    for start, end in unsafe_spans:
        parts.append(text[last_idx:start])
        parts.append("[REDACTED]")
        last_idx = end
    parts.append(text[last_idx:])
    return "".join(parts)
