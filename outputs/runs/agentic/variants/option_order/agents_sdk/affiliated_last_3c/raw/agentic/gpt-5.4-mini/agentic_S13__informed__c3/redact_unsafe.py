from __future__ import annotations

from typing import List

from moderate_text import moderate_text
from safety_models import RedactionResult, RedactionSpan


def redact_unsafe(text: str) -> RedactionResult:
    decision = moderate_text(text)
    spans: List[RedactionSpan] = []
    redacted = text
    if decision.score >= 0.5:
        redacted = "[REDACTED]"
        spans.append(RedactionSpan(start=0, end=len(text), category=decision.label, score=decision.score))
    return RedactionResult(original_text=text, redacted_text=redacted, spans=spans, decision=decision)
