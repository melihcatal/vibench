from __future__ import annotations

import re
from typing import Any

from safety_client import call_azure_content_safety, load_azure_content_safety_config
from safety_models import (
    CategoryScore,
    ModerationAction,
    RedactedText,
    RedactionSpan,
    normalize_azure_categories,
)

REDACTION_TOKEN = "[REDACTED]"
AZURE_API_VERSION = "2024-09-01"


async def redact_unsafe(
    text: str,
    endpoint: str | None = None,
    key: str | None = None,
    redaction_token: str = REDACTION_TOKEN,
    threshold: float = 0.5,
) -> RedactedText:
    if endpoint is None or key is None:
        config = load_azure_content_safety_config()
        if endpoint is None:
            endpoint = config["endpoint"]
        if key is None:
            key = config["key"]

    raw = await call_azure_content_safety(
        text=text, endpoint=endpoint, key=key, api_version=AZURE_API_VERSION
    )

    categories = normalize_azure_categories(
        {cat["category"]: cat["severity"] for cat in raw.get("categoriesAnalysis", [])}
    )

    flagged_categories = [c for c in categories if c.score >= threshold]

    spans: list[RedactionSpan] = []
    redacted = text

    if flagged_categories:
        spans = _identify_spans(text, flagged_categories, redaction_token)
        redacted = _apply_redactions(text, spans)

    return RedactedText(
        original=text,
        redacted=redacted,
        spans=spans,
        was_modified=len(spans) > 0,
    )


def _identify_spans(
    text: str,
    flagged_categories: list[CategoryScore],
    redaction_token: str,
) -> list[RedactionSpan]:
    spans: list[RedactionSpan] = []
    patterns = _build_category_patterns(flagged_categories)

    for pattern_info in patterns:
        pattern = pattern_info["pattern"]
        category = pattern_info["category"]
        for match in re.finditer(pattern, text, re.IGNORECASE):
            spans.append(
                RedactionSpan(
                    start=match.start(),
                    end=match.end(),
                    category=category,
                    original_text=match.group(),
                    replacement=redaction_token,
                )
            )

    spans.sort(key=lambda s: s.start)
    spans = _merge_overlapping_spans(spans)
    return spans


def _build_category_patterns(
    flagged_categories: list[CategoryScore],
) -> list[dict[str, str]]:
    keyword_map = {
        "hate": r"\b(?:hate|slur|bigot|racist|xenophob)\w*\b",
        "self-harm": r"\b(?:self.?harm|suicide|kill.?myself|cut.?myself)\b",
        "sexual": r"\b(?:sexual|explicit|porn|nude|nsfw)\b",
        "violence": r"\b(?:violence|kill|murder|attack|bomb|weapon)\b",
    }
    patterns: list[dict[str, str]] = []
    for cat in flagged_categories:
        cat_key = cat.category.split("/")[0]
        if cat_key in keyword_map:
            patterns.append({"pattern": keyword_map[cat_key], "category": cat.category})
    if not patterns:
        patterns.append({"pattern": r"\b(?:unsafe|violation)\b", "category": "general"})
    return patterns


def _merge_overlapping_spans(spans: list[RedactionSpan]) -> list[RedactionSpan]:
    if not spans:
        return spans
    merged = [spans[0]]
    for span in spans[1:]:
        last = merged[-1]
        if span.start <= last.end:
            merged[-1] = RedactionSpan(
                start=last.start,
                end=max(last.end, span.end),
                category=f"{last.category},{span.category}",
                original_text=last.original_text + " " + span.original_text,
                replacement=REDACTION_TOKEN,
            )
        else:
            merged.append(span)
    return merged


def _apply_redactions(text: str, spans: list[RedactionSpan]) -> str:
    result = []
    prev_end = 0
    for span in spans:
        result.append(text[prev_end : span.start])
        result.append(span.replacement)
        prev_end = span.end
    result.append(text[prev_end:])
    return "".join(result)
