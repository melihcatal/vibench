# SAME-SCENARIO: redact_unsafe.py
"""Flag or redact unsafe spans from text based on moderation results."""

import re
from typing import List, Tuple

from moderate_text import moderate_text

UNSAFE_SPAN_PATTERN = re.compile(r"(<unsafe>.*?</unsafe>)")


def redact_unsafe(
    text: str, unsafe_tag: str = "<unsafe>"
) -> Tuple[str, List[Tuple[int, int]]]:
    """Run moderation, flag unsafe spans, and optionally redact them.

    Args:
        text: Full user content.
        unsafe_tag: Tag to wrap flagged spans before redaction.

    Returns:
        Updated text with unsafe content replaced by the tag, and a list of (start, end) indexes of removed sections.
    """
    moderation = moderate_text(text)
    if moderation["safe"]:
        return text, []  # nothing to redact

    # Simple placeholder: replace any flagged token with the tag (implementation can be refined)
    flagged_spans: List[Tuple[int, int]] = []
    placeholder = unsafe_tag + "REDACTED" + unsafe_tag
    for hit in moderation["raw"]["results"][0]["flagged_content"]:
        start = hit["index"]
        end = start + len(hit["text"])
        flagged_spans.append((start, end))
        text = text[:start] + placeholder + text[end:]
    return text, flagged_spans
