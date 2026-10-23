# redact_unsafe.py
"""Flags or redacts unsafe spans from text (Azure AI Content Safety)"""

from safety_client import parse_response
from typing import List, Tuple


def redact_unsafe(text: str, unsafe_spans: List[Tuple[int, int]]) -> str:
    """Remove or mask unsafe content based on span offsets."""
    # Simple redaction: replace each unsafe span with asterisks of same length
    # Sort spans by start index descending to avoid offset shifts
    spans = sorted(unsafe_spans, key=lambda s: s[0], reverse=True)
    for start, end in spans:
        # Ensure indices are within bounds
        if 0 <= start < end <= len(text):
            # Replace with asterisks (or you could use a generic placeholder)
            text = text[:start] + "*" * (end - start) + text[end:]
    return text
