import re
from typing import List

def redact_unsafe(text: str, unsafe_spans: List[dict]) -> str:
    """Redact flagged unsafe spans from the original text.

    Each unsafe_span dict should contain 'start' and 'end' character offsets.
    This helper works with any provider's response format.
    """
    # Create a sorted list of (start, end, text) tuples
    spans = [(span['start'], span['end'], text[span['start']:span['end']]) for span in unsafe_spans]
    spans.sort(key=lambda x: x[0])
    # Build a new string skipping the unsafe portions
    redacted = []
    last_end = 0
    for start, end, _ in spans:
        if start > last_end:
            redacted.append(text[last_end:start])
        last_end = end
    if last_end < len(text):
        redacted.append(text[last_end:])
    return ''.join(redacted)
