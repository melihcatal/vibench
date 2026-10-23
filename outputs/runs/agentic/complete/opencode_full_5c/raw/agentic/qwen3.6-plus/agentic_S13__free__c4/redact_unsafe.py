import re
from safety_client import call_moderation, OPENAI_MODERATION_MODEL
from safety_models import (
    RedactionResult,
    ModerationResult,
    normalize_moderation_response,
    truncate_text,
    normalize_category_name,
)


def _split_into_spans(text, max_span_length=200):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    spans = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) > max_span_length and current:
            spans.append(current.strip())
            current = sentence
        else:
            current = current + " " + sentence if current else sentence
    if current.strip():
        spans.append(current.strip())
    if not spans and text:
        spans = [
            text[i : i + max_span_length] for i in range(0, len(text), max_span_length)
        ]
    return spans


def redact_unsafe(text, model=None, redaction_marker="[REDACTED]"):
    spans = _split_into_spans(text)
    flagged_spans = []
    categories_found = set()
    redacted_parts = []

    for span in spans:
        truncated = truncate_text(span)
        raw_response = call_moderation(
            truncated, model=model or OPENAI_MODERATION_MODEL
        )
        result = normalize_moderation_response(raw_response)
        if result.flagged:
            flagged_spans.append(span)
            for cat in result.categories:
                categories_found.add(cat)
            redacted_parts.append(redaction_marker)
        else:
            redacted_parts.append(span)

    redacted_text = " ".join(redacted_parts)
    return RedactionResult(
        original=text,
        redacted=redacted_text,
        flagged_spans=flagged_spans,
        categories_found=list(categories_found),
    )


def redact_unsafe_with_highlights(text, model=None, highlight_template="**[{}]**"):
    spans = _split_into_spans(text)
    flagged_spans = []
    categories_found = set()
    highlighted_parts = []

    for span in spans:
        truncated = truncate_text(span)
        raw_response = call_moderation(
            truncated, model=model or OPENAI_MODERATION_MODEL
        )
        result = normalize_moderation_response(raw_response)
        if result.flagged:
            flagged_spans.append(span)
            for cat in result.categories:
                categories_found.add(cat)
            label = ", ".join(result.categories[:3])
            highlighted_parts.append(highlight_template.format(label))
        else:
            highlighted_parts.append(span)

    highlighted_text = " ".join(highlighted_parts)
    return RedactionResult(
        original=text,
        redacted=highlighted_text,
        flagged_spans=flagged_spans,
        categories_found=list(categories_found),
    )
