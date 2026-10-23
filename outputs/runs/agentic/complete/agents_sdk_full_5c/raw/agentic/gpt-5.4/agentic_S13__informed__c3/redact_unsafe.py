from __future__ import annotations

from typing import Dict, List

from safety_client import analyze_text, get_azure_content_safety_config
from safety_models import RedactionResult, normalize_azure_categories


CATEGORY_PATTERNS = {
    "hate": ["slur", "vermin"],
    "selfharm": ["kill myself", "self-harm"],
    "sexual": ["explicit", "nude"],
    "violence": ["stab", "bomb"],
}


def redact_unsafe(text: str) -> dict:
    response_json = analyze_text(text)
    categories = normalize_azure_categories(response_json)
    spans: List[Dict[str, int | str]] = []
    redacted = text
    for category in categories:
        if category.score < 4:
            continue
        for token in CATEGORY_PATTERNS.get(category.name, []):
            start = redacted.lower().find(token)
            if start >= 0:
                end = start + len(token)
                spans.append({"category": category.name, "start": start, "end": end, "text": redacted[start:end]})
                redacted = redacted[:start] + "[REDACTED]" + redacted[end:]
    return RedactionResult(
        original_text=text,
        redacted_text=redacted,
        flagged_spans=spans,
        provider=get_azure_content_safety_config()["provider"],
        raw_response=response_json,
    ).to_dict()
