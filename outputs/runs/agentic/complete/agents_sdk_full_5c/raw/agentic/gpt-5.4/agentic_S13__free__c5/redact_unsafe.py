from __future__ import annotations

import re
from typing import Dict, List

from safety_client import OPENAI_MODERATION_MODEL, get_openai_client
from safety_models import RedactionResult


def redact_unsafe(text: str) -> RedactionResult:
    client = get_openai_client()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0].model_dump()
    flagged_categories: Dict[str, bool] = result.get("categories", {})

    patterns: List[tuple[str, str]] = []
    if flagged_categories.get("self-harm/instructions"):
        patterns.append((r"(?i)\b(how to kill myself|best suicide method|suicide instructions)\b", "[REDACTED_SELF_HARM_INSTRUCTIONS]"))
    if flagged_categories.get("hate") or flagged_categories.get("hate/threatening"):
        patterns.append((r"(?i)\b(slur|exterminate them|racial purity)\b", "[REDACTED_HATE]"))
    if flagged_categories.get("sexual/minors"):
        patterns.append((r"(?i)\b(underage sexual|child sexual)\b", "[REDACTED_CSAM]"))
    if flagged_categories.get("violence/graphic"):
        patterns.append((r"(?i)\b(gore|dismember|blood everywhere)\b", "[REDACTED_GRAPHIC_VIOLENCE]"))

    spans = []
    redacted = text
    for pattern, replacement in patterns:
        for match in re.finditer(pattern, redacted):
            spans.append({"start": match.start(), "end": match.end(), "text": match.group(0), "replacement": replacement})
        redacted = re.sub(pattern, replacement, redacted)

    return RedactionResult(
        provider="openai",
        original_text=text,
        redacted_text=redacted,
        flagged=bool(result.get("flagged", False)),
        spans=spans,
        raw=result,
    )
