import re
from typing import Tuple

def redact_unsafe(text: str, unsafe_spans: List[Tuple[int, int]]) -> str:
    """
    Replace each unsafe character span with a redaction token.
    Spans are zero‑based (start, end) and are assumed non‑overlapping.
    """
    # Sort spans by start descending to avoid shifting indexes
    for start, end in sorted(unsafe_spans, key=lambda s: s[0], reverse=True):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text

# Example helper to detect unsafe words (placeholder)
def detect_unsafe_spans(text: str) -> List[Tuple[int, int]]:
    # Simple regex for demonstration (detects URLs as unsafe)
    urls = [(m.start(), m.end()) for m in re.finditer(r'https?://\S+', text)]
    return urls
