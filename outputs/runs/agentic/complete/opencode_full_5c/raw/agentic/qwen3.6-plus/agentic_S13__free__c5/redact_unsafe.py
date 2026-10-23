import re
from safety_client import get_openai_client, MODERATION_MODEL
from safety_models import RedactionResult, ModerationResult, parse_moderation_response


def split_into_spans(text: str, max_span_length: int = 200) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    spans = []
    current_span = ""
    for sentence in sentences:
        if len(current_span) + len(sentence) > max_span_length and current_span:
            spans.append(current_span.strip())
            current_span = sentence
        else:
            current_span = (" " + current_span if current_span else "") + sentence
    if current_span.strip():
        spans.append(current_span.strip())
    if not spans and text:
        spans = [
            text[i : i + max_span_length] for i in range(0, len(text), max_span_length)
        ]
    return spans


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> RedactionResult:
    if not text.strip():
        return RedactionResult(original_text=text, redacted_text=text, unsafe=False)

    client = get_openai_client()
    spans = split_into_spans(text)
    flagged_spans = []
    redacted_text = text

    for span in spans:
        response = client.moderations.create(
            model=MODERATION_MODEL,
            input=span,
        )
        raw = response.model_dump()
        result = parse_moderation_response(span, raw)

        if result.flagged:
            flagged_categories = [c.category for c in result.categories if c.flagged]
            flagged_spans.append(
                {
                    "text": span,
                    "categories": flagged_categories,
                    "highest_score": result.highest_score,
                }
            )
            redacted_text = redacted_text.replace(span, replacement)

    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        unsafe=len(flagged_spans) > 0,
    )


def flag_unsafe_spans(text: str) -> list[dict]:
    result = redact_unsafe(text)
    return result.flagged_spans


def get_redacted_text(text: str, replacement: str = "[REDACTED]") -> str:
    result = redact_unsafe(text, replacement)
    return result.redacted_text
