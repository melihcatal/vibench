from safety_client import prepare_text_payload, post_perspective
from safety_models import (
    RedactionResult,
    RedactionSpan,
    normalize_score,
    normalize_text,
)


def redact_unsafe(text, language=None):
    original = normalize_text(text)
    raw = post_perspective(prepare_text_payload(original, language))
    score = normalize_score(
        raw.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
    )
    if score < 0.5:
        return RedactionResult(text=original, spans=[], raw=raw)
    spans = [RedactionSpan(start=0, end=len(original), label="TOXICITY")]
    return RedactionResult(text="[REDACTED]", spans=spans, raw=raw)
