"""
[SAME-SCENARIO] redact_unsafe.py
Flags or redacts unsafe spans from text.
Uses the OpenAI Moderation API via the openai SDK (text-moderation-latest model).
"""

import re
from typing import Optional

from safety_client import get_openai_client, call_moderation_api
from safety_models import ModerationResponse, normalize_moderation_result


def _find_unsafe_spans(
    text: str,
    flagged_categories: list[str],
    window_size: int = 80,
) -> list[tuple[int, int, str]]:
    """
    Approximate unsafe span detection using sentence splitting and keyword heuristics
    informed by the flagged categories from OpenAI moderation.

    The moderation API returns document-level flags; we approximate span-level
    redaction by identifying sentences containing high-risk keywords.

    Args:
        text: Original text.
        flagged_categories: List of flagged category names from OpenAI moderation.
        window_size: Character window size for span extraction.

    Returns:
        List of (start, end, replacement_text) tuples for unsafe spans.
    """
    category_keywords = {
        "sexual": [
            r"(?:explicit|sexual|pornographic|nude|naked|sex|intercourse)",
        ],
        "hate": [
            r"(?:(?:hate|slur|racist|bigot|derogatory)(?:\s+(?:speech|remark|term))?)",
        ],
        "harassment": [
            r"(?:(?:harass|bully|threaten|intimidate|stalk)(?:ed|ing|ment)?)",
        ],
        "self-harm": [
            r"(?:(?:suicide|self.?harm|self.?injur|cutting|overdose)(?:s|d|ing)?)",
        ],
        "violence": [
            r"(?:(?:kill|murder|violence|blood|gore|weapon|shoot|stab)(?:ed|ing|s)?)",
        ],
        "harassment/threatening": [
            r"(?:(?:threat|threaten|will.?hurt|going.?to.?hurt|make.?you.?pay))",
        ],
        "violence/graphic": [
            r"(?:(?:gore|torture|mutilat|dismember|sever)(?:ed|ing|ion)?)",
        ],
        "self-harm/intent": [
            r"(?:(?:want.?to.?die|kill.?myself|end.?it.?all|can.?t.?go.?on))",
        ],
    }

    sentences = re.split(r'(?<=[.!?])\s+', text)
    spans = []
    current_pos = 0

    for sentence in sentences:
        sentence_lower = sentence.lower()
        matched = False

        for category in flagged_categories:
            base_category = category.split("/")[0]
            patterns = category_keywords.get(category, category_keywords.get(base_category, []))
            for pattern in patterns:
                if re.search(pattern, sentence_lower):
                    matched = True
                    break
            if matched:
                break

        if matched:
            start = current_pos
            end = current_pos + len(sentence)
            replacement = "[REDACTED]"
            spans.append((start, end, replacement))

        current_pos += len(sentence) + 1

    return spans


def redact_unsafe_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
    replacement: str = "[REDACTED]",
) -> tuple[str, bool, list[tuple[int, int, str]]]:
    """
    Flag and redact unsafe spans from text using OpenAI Moderation API
    to detect unsafe content and heuristics to locate spans.

    Args:
        text: The text to redact.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI moderation model identifier (default: text-moderation-latest).
        replacement: String to replace unsafe spans with.

    Returns:
        Tuple of (redacted_text, was_flagged, list of (start, end, replacement) spans).
    """
    client = get_openai_client(api_key=api_key)
    raw_result = call_moderation_api(client, text, model=model)
    normalized = normalize_moderation_result(raw_result)

    if not normalized.flagged:
        return text, False, []

    flagged_categories = [
        c.category for c in normalized.categories if c.flagged
    ]
    spans = _find_unsafe_spans(text, flagged_categories)

    if not spans:
        if normalized.flagged:
            return replacement, True, [(0, len(text), replacement)]
        return text, False, []

    redacted = []
    last_end = 0
    updated_spans = []

    for start, end, _ in spans:
        redacted.append(text[last_end:start])
        redacted.append(replacement)
        updated_spans.append((start, end, replacement))
        last_end = end

    redacted.append(text[last_end:])

    return "".join(redacted), True, updated_spans


def flag_unsafe_spans(
    text: str,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> list[dict]:
    """
    Flag unsafe spans without redacting. Returns metadata about each unsafe region.

    Args:
        text: The text to scan.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of dicts with keys: start, end, span_text, categories.
    """
    _, flagged, spans = redact_unsafe_text(text, api_key=api_key, model=model)

    if not flagged:
        return []

    flagged_categories = []
    client = get_openai_client(api_key=api_key)
    raw_result = call_moderation_api(client, text, model=model)
    normalized = normalize_moderation_result(raw_result)
    flagged_categories = [c.category for c in normalized.categories if c.flagged]

    return [
        {
            "start": start,
            "end": end,
            "span_text": text[start:end],
            "categories": flagged_categories,
        }
        for start, end, _ in spans
    ]
