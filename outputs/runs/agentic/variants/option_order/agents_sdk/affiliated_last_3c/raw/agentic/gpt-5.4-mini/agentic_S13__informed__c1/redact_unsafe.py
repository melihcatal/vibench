from __future__ import annotations

from typing import List, Tuple

from safety_models import RedactionResult, SafetyModerationRequest
from moderate_text import moderate_text


MASK = "[REDACTED]"


def redact_unsafe(text: str) -> RedactionResult:
    decision = moderate_text(SafetyModerationRequest(text=text))
    spans: List[Tuple[int, int, str]] = []
    redacted = text
    if decision.flagged:
        redacted = MASK
        spans.append((0, len(text), "unsafe"))
    return RedactionResult(text=redacted, spans=spans, flagged=decision.flagged, provider=decision.provider)
