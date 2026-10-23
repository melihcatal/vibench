# [SAME-SCENARIO] redact_unsafe.py
# Flags or redacts unsafe spans from text

import re
from typing import List, Tuple
from safety_client import TextSafetyClient


def redact_unsafe(text: str, unsafe_pattern: str = r"[Uu]nsafe") -> str:
    """Replace any detected unsafe spans in the input text with a placeholder.

    Args:
        text: User message to process.
        unsafe_pattern: Regex pattern that matches text flagged as unsafe.

    Returns:
        Text with unsafe spans replaced by '[REDACTED]'.
    """
    # Example: use provider's flagged unsafe span list if available
    client = TextSafetyClient()
    flags = client.get_unsafe_spans(text)
    # flags is a list of (start, end) tuples
    if not flags:
        return text
    # Sort spans by start descending to avoid offset shift while replacing
    for start, end in sorted(flags, key=lambda x: x[0], reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text
