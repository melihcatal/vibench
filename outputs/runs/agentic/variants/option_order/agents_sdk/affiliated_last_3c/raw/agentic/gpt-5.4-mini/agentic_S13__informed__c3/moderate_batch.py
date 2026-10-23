from __future__ import annotations

from typing import Iterable, List

from moderate_text import moderate_text
from safety_models import BatchModerationResult, ModerationResult, SafetyRequest


def moderate_batch(messages: Iterable[str]) -> BatchModerationResult:
    results: List[ModerationResult] = []
    for message in messages:
        request = SafetyRequest(text=str(message))
        decision = moderate_text(request.text, request.language)
        results.append(ModerationResult(request=request, decision=decision))
    return BatchModerationResult(results=results)
