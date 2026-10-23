import re

from safety_models import (
    SafetyCategory,
    SafetyRequest,
    RedactionResult,
    FlaggedSpan,
    CategoryScore,
    SeverityLevel,
)
from safety_client import call_azure_content_safety, parse_response


def _find_unsafe_segments(text: str, response: SafetyResponse) -> list[FlaggedSpan]:
    flagged_spans = []

    for score in response.category_scores:
        if score.severity.value < SeverityLevel.LOW.value:
            continue

        category = score.category
        category_keywords = _get_category_keywords(category)

        for keyword in category_keywords:
            for match in re.finditer(re.escape(keyword), text, re.IGNORECASE):
                flagged_spans.append(
                    FlaggedSpan(
                        start=match.start(),
                        end=match.end(),
                        category=category,
                        severity=score.severity,
                        matched_text=match.group(),
                    )
                )

    flagged_spans.sort(key=lambda s: s.start)
    merged = _merge_overlapping_spans(flagged_spans)
    return merged


def _get_category_keywords(category: SafetyCategory) -> list[str]:
    keywords_map = {
        SafetyCategory.HATE: [],
        SafetyCategory.SELF_HARM: [],
        SafetyCategory.SEXUAL: [],
        SafetyCategory.VIOLENCE: [],
    }
    return keywords_map.get(category, [])


def _merge_overlapping_spans(spans: list[FlaggedSpan]) -> list[FlaggedSpan]:
    if not spans:
        return spans

    merged = [spans[0]]
    for span in spans[1:]:
        last = merged[-1]
        if span.start <= last.end:
            last.end = max(last.end, span.end)
            last.matched_text = span.matched_text
            if span.severity.value > last.severity.value:
                last.severity = span.severity
        else:
            merged.append(span)

    return merged


def redact_unsafe(
    text: str,
    categories: list[SafetyCategory] | None = None,
    replacement: str = "[REDACTED]",
) -> RedactionResult:
    if categories is None:
        categories = list(SafetyCategory)

    request = SafetyRequest(text=text, categories=categories)
    response = call_azure_content_safety(request)

    flagged_spans = _find_unsafe_segments(text, response)

    redacted = text
    offset = 0
    for span in flagged_spans:
        adj_start = span.start + offset
        adj_end = span.end + offset
        redacted = redacted[:adj_start] + replacement + redacted[adj_end:]
        offset += len(replacement) - (span.end - span.start)

    return RedactionResult(
        original_text=text,
        redacted_text=redacted,
        flagged_spans=flagged_spans,
        category_scores=response.category_scores,
    )


def flag_unsafe_spans(
    text: str,
    categories: list[SafetyCategory] | None = None,
) -> dict:
    result = redact_unsafe(text, categories)

    return {
        "original_text": result.original_text,
        "redacted_text": result.redacted_text,
        "flagged_count": len(result.flagged_spans),
        "flagged_spans": [
            {
                "start": s.start,
                "end": s.end,
                "category": s.category.value,
                "severity": s.severity.name,
                "matched_text": s.matched_text,
            }
            for s in result.flagged_spans
        ],
        "category_scores": [
            {
                "category": c.category.value,
                "severity": c.severity.name,
                "score": c.raw_score,
            }
            for c in result.category_scores
        ],
    }
