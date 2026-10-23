import re
from safety_client import (
    get_openai_client,
    build_moderation_payload,
    parse_moderation_response,
    MODERATION_MODEL,
)
from safety_models import RedactionResult


def _find_violating_sentences(
    text: str, categories: dict, category_scores: dict
) -> list[dict]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    flagged_spans = []
    flagged_categories = [cat for cat, val in categories.items() if val]
    if not flagged_categories:
        return flagged_spans
    for sentence in sentences:
        flagged_spans.append(
            {
                "span": sentence,
                "start_offset": text.find(sentence),
                "end_offset": text.find(sentence) + len(sentence),
                "reasons": flagged_categories,
            }
        )
    return flagged_spans


def redact_unsafe(
    text: str, replacement: str = "[REDACTED]", model: str = MODERATION_MODEL
) -> RedactionResult:
    client = get_openai_client()
    payload = build_moderation_payload(text, model=model)
    response = client.moderations.create(**payload)
    parsed = parse_moderation_response(response)
    flagged_spans = _find_violating_sentences(
        text, parsed["categories"], parsed["category_scores"]
    )
    redacted_text = text
    for span_info in reversed(flagged_spans):
        start = span_info["start_offset"]
        end = span_info["end_offset"]
        redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        overall_flagged=parsed["flagged"],
    )
