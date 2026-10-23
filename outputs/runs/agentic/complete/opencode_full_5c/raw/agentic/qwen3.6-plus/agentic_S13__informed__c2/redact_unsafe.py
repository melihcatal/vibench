import re

from safety_client import analyze_text
from safety_models import (
    AZURE_CONTENT_SAFETY_CATEGORIES,
    FlaggedSpan,
    RedactionResult,
)


def _find_flagged_spans(text: str, flagged_categories: list[str]) -> list[FlaggedSpan]:
    spans: list[FlaggedSpan] = []
    for category in flagged_categories:
        category_lower = category.lower()
        patterns = [
            re.compile(re.escape(category_lower), re.IGNORECASE),
        ]
        if category_lower == "hate":
            patterns.extend(
                [
                    re.compile(r"\b(hate|hatred|bigot)\b", re.IGNORECASE),
                ]
            )
        elif category_lower == "selfharm":
            patterns.extend(
                [
                    re.compile(r"\b(self.harm|suicide|self.injury)\b", re.IGNORECASE),
                ]
            )
        elif category_lower == "sexual":
            patterns.extend(
                [
                    re.compile(r"\b(explicit|nsfw|adult content)\b", re.IGNORECASE),
                ]
            )
        elif category_lower == "violence":
            patterns.extend(
                [
                    re.compile(r"\b(violence|kill|attack|weapon)\b", re.IGNORECASE),
                ]
            )

        for pattern in patterns:
            for match in pattern.finditer(text):
                spans.append(
                    FlaggedSpan(
                        start=match.start(),
                        end=match.end(),
                        category=category,
                        score=1.0,
                        original_text=match.group(),
                    )
                )

    seen = set()
    unique_spans = []
    for span in spans:
        key = (span.start, span.end, span.category)
        if key not in seen:
            seen.add(key)
            unique_spans.append(span)

    return sorted(unique_spans, key=lambda s: s.start)


def redact_unsafe(
    text: str,
    replacement: str = "[REDACTED]",
    min_severity: int = 2,
) -> RedactionResult:
    result = analyze_text(text, AZURE_CONTENT_SAFETY_CATEGORIES)

    if result.is_safe:
        return RedactionResult(
            original_text=text,
            redacted_text=text,
            flagged_spans=[],
            is_safe=True,
        )

    flagged_spans = _find_flagged_spans(text, result.flagged_categories)

    if not flagged_spans:
        return RedactionResult(
            original_text=text,
            redacted_text=text,
            flagged_spans=[],
            is_safe=False,
        )

    redacted = text
    offset = 0
    for span in sorted(flagged_spans, key=lambda s: s.start):
        adj_start = span.start + offset
        adj_end = span.end + offset
        redacted = redacted[:adj_start] + replacement + redacted[adj_end:]
        offset += len(replacement) - (span.end - span.start)

    return RedactionResult(
        original_text=text,
        redacted_text=redacted,
        flagged_spans=flagged_spans,
        is_safe=False,
    )
