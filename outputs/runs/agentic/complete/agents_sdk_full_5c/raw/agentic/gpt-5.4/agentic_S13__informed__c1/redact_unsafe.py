from __future__ import annotations

from typing import Iterable, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import RedactionResult, normalize_perspective_scores


def _apply_redactions(text: str, spans: list[dict], replacement: str) -> str:
    if not spans:
        return text
    ordered = sorted(spans, key=lambda item: item["begin"])
    parts = []
    cursor = 0
    for span in ordered:
        start = int(span["begin"])
        end = int(span["end"])
        if start < cursor:
            continue
        parts.append(text[cursor:start])
        parts.append(replacement)
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts)


def redact_unsafe(
    text: str,
    *,
    attributes: Optional[Iterable[str]] = None,
    language: str = "en",
    span_threshold: float = 0.7,
    replacement: str = "[REDACTED]",
) -> RedactionResult:
    client = PerspectiveSafetyClient()
    response = client.analyze_text(
        text=text,
        attributes=attributes,
        language=language,
        span_annotations=True,
    )
    categories = normalize_perspective_scores(response.get("attributeScores", {}))
    spans = []
    for attribute_name, payload in response.get("attributeScores", {}).items():
        for span in payload.get("spanScores", []):
            score = float(span.get("score", {}).get("value", 0.0))
            if score >= span_threshold:
                spans.append(
                    {
                        "category": attribute_name,
                        "begin": int(span.get("begin", 0)),
                        "end": int(span.get("end", 0)),
                        "score": score,
                    }
                )
    redacted_text = _apply_redactions(text, spans, replacement)
    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=spans,
        categories=categories,
        raw_response=response,
    )
