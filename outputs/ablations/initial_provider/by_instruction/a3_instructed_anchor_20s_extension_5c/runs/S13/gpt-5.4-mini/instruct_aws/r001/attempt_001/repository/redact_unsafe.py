from typing import Any, Dict, List

from moderate_text import moderate_text
from safety_models import RedactionResult


def redact_unsafe(text: str, thresholds: Dict[str, Any] | None = None) -> RedactionResult:
    decision = moderate_text(text, thresholds=thresholds)
    if decision.allowed:
        return RedactionResult(text=text, spans=[], allowed=True)
    spans: List[Dict[str, Any]] = [{"start": 0, "end": len(text), "category": decision.category, "score": decision.score}]
    return RedactionResult(text="[REDACTED]", spans=spans, allowed=False)
