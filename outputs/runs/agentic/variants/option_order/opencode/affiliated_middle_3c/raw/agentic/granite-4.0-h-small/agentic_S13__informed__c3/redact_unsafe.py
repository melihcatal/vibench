import re
from typing import List


# Using IBM watsonx.ai guardrails tokenization/spans (same-scenario)
def redact_unsafe(text: str, unsafe_spans: List[tuple]) -> str:
    """Redacts flagged unsafe character spans from text.

    Args:
        text (str): Original message.
        unsafe_spans (List[tuple]): List of (start, end) character index tuples to redact.

    Returns:
        str: Text with unsafe spans replaced with [REDACTED].
    """
    # Sort spans by start descending to avoid shifting indices
    for start, end in sorted(unsafe_spans, key=lambda x: x[0], reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text


# Example simple matcher used by the provider's response normalization (local helper would provide)
def find_unsafe_spans(tokenized: str) -> List[tuple]:
    """Stub placeholder for demonstration."""
    # Example: redact profanity pattern
    pattern = re.compile(r"\b(badword1|badword2)\b", re.IGNORECASE)
    matches = pattern.finditer(tokenized)
    return [(m.start(), m.end()) for m in matches]
