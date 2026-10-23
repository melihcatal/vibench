from __future__ import annotations

from safety_client import SafetyClient
from safety_models import RedactionResult, RedactionSpan, TextSafetyRequest


client = SafetyClient()


def redact_unsafe(text: str) -> RedactionResult:
    decision = client.analyze_text(TextSafetyRequest(text=text, categories=["Hate", "SelfHarm", "Sexual", "Violence"]))
    spans = []
    redacted = text
    if not decision.allowed:
        spans.append(RedactionSpan(start=0, end=len(text), label="unsafe_text"))
        redacted = "[REDACTED]"
    return RedactionResult(text=redacted, spans=spans, decision=decision)
