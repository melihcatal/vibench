from typing import List

from safety_client import moderate_text_openai
from safety_models import RedactionResult, RedactionSpan


def redact_unsafe(text: str) -> RedactionResult:
    decision = moderate_text_openai(text)
    spans: List[RedactionSpan] = []
    if decision.flagged:
        spans.append(RedactionSpan(start=0, end=len(text), label="unsafe"))
        return RedactionResult(text="[REDACTED]" if text else text, spans=spans)
    return RedactionResult(text=text, spans=spans)
