from __future__ import annotations

import re
from typing import Dict, List

from safety_client import get_openai_client, moderation_model
from safety_models import RedactionResult, normalize_openai_moderation_result


CATEGORY_PATTERNS: Dict[str, List[str]] = {
    "hate": [r"\bslur\b", r"\bsubhuman\b"],
    "harassment": [r"\bidiot\b", r"\bkill yourself\b"],
    "violence": [r"\bshoot\b", r"\bstab\b", r"\bbomb\b"],
    "self-harm": [r"\bsuicide\b", r"\bcut myself\b"],
    "sexual": [r"\bexplicit sex\b", r"\bchild porn\b"],
}


def redact_unsafe(text: str, api_key: str | None = None, model: str | None = None, replacement: str = "[REDACTED]") -> RedactionResult:
    client = get_openai_client(api_key)
    resolved_model = moderation_model(model)
    response = client.moderations.create(
        model=resolved_model,
        input=text,
    )
    moderation = normalize_openai_moderation_result(response.results[0], model=resolved_model)
    redacted = text
    spans = []
    if moderation.flagged:
        for category, flagged in moderation.categories.items():
            if not flagged:
                continue
            for pattern in CATEGORY_PATTERNS.get(category, []):
                for match in re.finditer(pattern, redacted, flags=re.IGNORECASE):
                    spans.append(
                        {
                            "category": category,
                            "start": match.start(),
                            "end": match.end(),
                            "text": match.group(0),
                        }
                    )
                redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)
    return RedactionResult(
        provider="openai",
        model=resolved_model,
        original_text=text,
        redacted_text=redacted,
        flagged=moderation.flagged,
        categories=moderation.categories,
        spans=spans,
        raw=moderation.raw,
    )
