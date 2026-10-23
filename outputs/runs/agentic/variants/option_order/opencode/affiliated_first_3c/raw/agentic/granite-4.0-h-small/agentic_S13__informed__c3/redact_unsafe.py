# [SAME-SCENARIO] redact_unsafe.py

import re
from safety_client import TextSafetyClient


def redact_unsafe_spans(text: str) -> str:
    """Flags or redacts unsafe spans from the supplied text.

    The function requests safety analysis, extracts any flagged unsafe
    span information from the provider response, and replaces those
    regions with '[REDACTED]'.
    """
    client = TextSafetyClient()
    analysis = client.analyze(text)
    # Example: assume analysis contains a list of unsafe_spans with start/end indices
    unsafe_spans = analysis.get("unsafe_spans", [])
    # Sort spans by start to avoid index shifts when replacing
    unsafe_spans.sort(key=lambda s: s["start"])
    # Build a mapping of replacement regions
    replacements = []
    offset = 0
    for span in unsafe_spans:
        start = span["start"] + offset
        end = span["end"] + offset
        replacements.append((start, end, "[REDACTED]"))
        offset += len("[REDACTED]") - (end - start)
    # Apply replacements backwards to keep indices stable
    replacements.reverse()
    result = list(text)
    for start, end, rep in replacements:
        result[start:end] = list(rep)
    return "".join(result)
