import re
from safety_client import (
    get_openai_client,
    validate_text_input,
    OPENAI_MODERATION_MODEL,
)
from safety_models import RedactionResult


REDACTION_MARKER = "[REDACTED]"


def _split_into_segments(text, segment_length=100, overlap=20):
    if len(text) <= segment_length:
        return [text]
    segments = []
    start = 0
    while start < len(text):
        end = start + segment_length
        if end < len(text):
            while end > start and text[end] not in (" ", ".", ",", "!", "?", "\n"):
                end -= 1
            if end <= start:
                end = start + segment_length
        segment = text[start:end]
        segments.append(segment)
        start = end - overlap
    return segments


def _get_flagged_segments(text, client):
    segments = _split_into_segments(text)
    flagged = []
    for seg in segments:
        response = client.moderations.create(
            input=seg,
            model=OPENAI_MODERATION_MODEL,
        )
        result = response.results[0]
        if result.flagged:
            cats = {k: v for k, v in result.categories.items() if v}
            flagged.append(
                {
                    "segment": seg,
                    "categories": cats,
                    "scores": {k: v for k, v in result.category_scores.items()},
                }
            )
    return flagged


def redact_unsafe(text, redaction_marker=REDACTION_MARKER):
    validated = validate_text_input(text)
    client = get_openai_client()
    response = client.moderations.create(
        input=validated,
        model=OPENAI_MODERATION_MODEL,
    )
    result = response.results[0]
    if not result.flagged:
        return RedactionResult(
            original_text=validated,
            redacted_text=validated,
            flagged_segments=[],
            categories_triggered=[],
        )
    flagged_segments = _get_flagged_segments(validated, client)
    redacted = validated
    categories_triggered = set()
    for seg_info in flagged_segments:
        seg_text = seg_info["segment"]
        escaped = re.escape(seg_text)
        redacted = re.sub(escaped, redaction_marker, redacted, count=1)
        categories_triggered.update(seg_info["categories"].keys())
    return RedactionResult(
        original_text=validated,
        redacted_text=redacted,
        flagged_segments=flagged_segments,
        categories_triggered=sorted(categories_triggered),
    )


def redact_unsafe_full(text, redaction_marker=REDACTION_MARKER):
    validated = validate_text_input(text)
    client = get_openai_client()
    response = client.moderations.create(
        input=validated,
        model=OPENAI_MODERATION_MODEL,
    )
    result = response.results[0]
    if not result.flagged:
        return RedactionResult(
            original_text=validated,
            redacted_text=validated,
            flagged_segments=[],
            categories_triggered=[],
        )
    words = validated.split()
    redacted_words = []
    categories_triggered = set()
    for word in words:
        word_response = client.moderations.create(
            input=word,
            model=OPENAI_MODERATION_MODEL,
        )
        word_result = word_response.results[0]
        if word_result.flagged:
            redacted_words.append(redaction_marker)
            cats = {k: v for k, v in word_result.categories.items() if v}
            categories_triggered.update(cats.keys())
        else:
            redacted_words.append(word)
    redacted = " ".join(redacted_words)
    return RedactionResult(
        original_text=validated,
        redacted_text=redacted,
        flagged_segments=[
            {"word": w, "redacted": True} for w in words if w not in redacted_words
        ],
        categories_triggered=sorted(categories_triggered),
    )
