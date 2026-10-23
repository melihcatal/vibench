"""
[SAME-SCENARIO] redact_unsafe.py - Flags or redacts unsafe spans from text.

Uses the OpenAI Moderations API (model: omni-moderation-latest) to identify
policy-violating categories and redacts or masks the corresponding spans
based on detected severity levels.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from safety_client import SafetyClient
from safety_models import CategoryScore, ModerationResult, SeverityLevel


# Thresholds that map to redaction actions
_REDACTION_THRESHOLDS = {
    SeverityLevel.CRITICAL: "***REDACTED***",
    SeverityLevel.HIGH: "***REDACTED***",
    SeverityLevel.MEDIUM: "[FILTERED]",
    SeverityLevel.LOW: "[CAUTION]",
    SeverityLevel.SAFE: None,
}


def _span_heuristic(text: str, category_scores: List[CategoryScore]) -> List[Tuple[int, int]]:
    """
    Heuristic span detection: flag sentences that likely contain the highest-risk
    categories. This is a local heuristic used alongside OpenAI moderation scores.
    """
    flagged_spans: List[Tuple[int, int]] = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    pos = 0
    for sentence in sentences:
        if any(cs.flagged for cs in category_scores):
            flagged_spans.append((pos, pos + len(sentence)))
        pos += len(sentence) + 1
    return flagged_spans


def redact_unsafe(
    text: str,
    api_key: Optional[str] = None,
    redaction_strategy: str = "mask",
) -> str:
    """
    Evaluate text via OpenAI moderation and redact unsafe spans.

    Parameters
    ----------
    text : str
        The input text to evaluate and redact.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var if not provided.
    redaction_strategy : str
        One of 'mask' (replace with markers) or 'remove' (delete flagged spans).

    Returns
    -------
    str
        The text with unsafe spans redacted or flagged.
    """
    if not text or not text.strip():
        return text

    client = SafetyClient(api_key=api_key)
    try:
        result = client.moderate_single(text)
    finally:
        client.close()

    if not result.flagged:
        return text

    replacement = _REDACTION_THRESHOLDS.get(result.severity, "[FILTERED]")
    if replacement is None:
        return text

    flagged_spans = _span_heuristic(text, result.category_scores)
    if not flagged_spans:
        return text

    if redaction_strategy == "remove":
        return _remove_spans(text, flagged_spans)
    return _mask_spans(text, flagged_spans, replacement or "[FILTERED]")


def _mask_spans(text: str, spans: List[Tuple[int, int]], replacement: str) -> str:
    """Replace flagged spans with a redaction marker."""
    parts: List[str] = []
    prev_end = 0
    for start, end in spans:
        parts.append(text[prev_end:start])
        parts.append(replacement)
        prev_end = end
    parts.append(text[prev_end:])
    return "".join(parts)


def _remove_spans(text: str, spans: List[Tuple[int, int]]) -> str:
    """Remove flagged spans entirely."""
    parts: List[str] = []
    prev_end = 0
    for start, end in spans:
        parts.append(text[prev_end:start])
        prev_end = end
    parts.append(text[prev_end:])
    return " ".join(p for p in parts if p.strip())


def flag_unsafe(
    text: str,
    api_key: Optional[str] = None,
) -> dict:
    """
    Return a dict with flagging details without modifying the text.
    """
    if not text or not text.strip():
        return {"flagged": False, "text": text, "categories": [], "severity": "safe"}

    client = SafetyClient(api_key=api_key)
    try:
        result = client.moderate_single(text)
    finally:
        client.close()

    return {
        "flagged": result.flagged,
        "text": text,
        "categories": [
            cs.category for cs in result.category_scores if cs.flagged
        ],
        "severity": result.severity.value,
    }


def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python redact_unsafe.py <text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    redacted = redact_unsafe(text)
    print(f"Original: {text}")
    print(f"Redacted: {redacted}")


if __name__ == "__main__":
    main()
