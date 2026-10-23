from __future__ import annotations

import re
from typing import List

from safety_client import DEFAULT_MODERATION_MODEL, get_openai_client
from safety_models import RedactionResult, normalize_openai_result


_REDACTION_PATTERNS = {
    "hate": [r"\bslur\b"],
    "harassment": [r"\bidiot\b", r"\bkill yourself\b"],
    "self-harm": [r"\bsuicide\b", r"\bself harm\b"],
    "violence": [r"\bkill\b", r"\bstab\b", r"\bshoot\b"],
    "sexual": [r"\bexplicit\b"],
}


def redact_unsafe(text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(model=DEFAULT_MODERATION_MODEL, input=text)
    decision = normalize_openai_result(response.results[0], model=DEFAULT_MODERATION_MODEL)

    redacted = text
    matched_categories: List[str] = []
    for category in decision.categories:
        if not category.flagged:
            continue
        for pattern in _REDACTION_PATTERNS.get(category.name.split("/")[0], []):
            updated = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
            if updated != redacted and category.name not in matched_categories:
                matched_categories.append(category.name)
            redacted = updated

    if decision.flagged and redacted == text:
        redacted = "[CONTENT REDACTED]"
        matched_categories = [c.name for c in decision.categories if c.flagged]

    return RedactionResult(
        provider="OpenAI",
        original_text=text,
        redacted_text=redacted,
        flagged=decision.flagged,
        categories=matched_categories,
    ).to_dict()
