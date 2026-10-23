import re
from typing import List


def redact_unsafe(text: str, unsafe_spans: List[dict]) -> str:
    """Replace characters in each unsafe span with a redaction marker.

    unsafe_spans is expected to be the output format from the safety scoring service,
    e.g. [{"beginIndex": 5, "endIndex": 12}]. Each span is treated as inclusive start
    and exclusive end index.
    """
    # Sort spans by start index descending to avoid shifting indexes after replacements
    for span in sorted(unsafe_spans, key=lambda s: s["beginIndex"], reverse=True):
        start = span["beginIndex"]
        end = span["endIndex"]
        # Replace the span with asterisks (or any marker you prefer)
        text = text[:start] + "*" * (end - start) + text[end:]
    return text
