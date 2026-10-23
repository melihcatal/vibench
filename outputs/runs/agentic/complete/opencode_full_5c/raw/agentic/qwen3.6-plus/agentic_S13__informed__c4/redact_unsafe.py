import re
from azure.ai.contentsafety import ContentSafetyClient
from safety_client import (
    get_content_safety_client,
    build_analyze_text_payload,
    parse_analyze_text_response,
)
from safety_models import RedactionResult


def redact_unsafe(
    text: str,
    categories: list[str] | None = None,
    replacement: str = "[REDACTED]",
    client: ContentSafetyClient | None = None,
) -> RedactionResult:
    if client is None:
        client = get_content_safety_client()
    payload = build_analyze_text_payload(text=text, categories=categories)
    response = client.analyze_text(payload)
    parsed = parse_analyze_text_response(response)
    flagged_categories = [
        cat_name
        for cat_name, cat_info in parsed["categories"].items()
        if cat_info["severity_value"] >= 2
    ]
    if not flagged_categories:
        return RedactionResult(
            original_text=text,
            redacted_text=text,
            flagged_spans=[],
            categories_triggered=[],
        )
    sentences = re.split(r"(?<=[.!?])\s+", text)
    redacted_parts = []
    flagged_spans = []
    categories_triggered_set = set()
    for sentence in sentences:
        sentence_payload = build_analyze_text_payload(
            text=sentence, categories=categories
        )
        sentence_response = client.analyze_text(sentence_payload)
        sentence_parsed = parse_analyze_text_response(sentence_response)
        sentence_flagged = [
            cat_name
            for cat_name, cat_info in sentence_parsed["categories"].items()
            if cat_info["severity_value"] >= 2
        ]
        if sentence_flagged:
            redacted_parts.append(replacement)
            flagged_spans.append(
                {
                    "original": sentence,
                    "categories": sentence_flagged,
                    "highest_severity": sentence_parsed["highest_severity"],
                }
            )
            categories_triggered_set.update(sentence_flagged)
        else:
            redacted_parts.append(sentence)
    redacted_text = " ".join(redacted_parts)
    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        categories_triggered=sorted(categories_triggered_set),
    )
