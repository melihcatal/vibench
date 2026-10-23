from __future__ import annotations

from typing import Dict, Any

from safety_client import SafetyClient
from safety_models import ModerationDecision, ModerationRequest, redact_spans


def redact_unsafe(request: ModerationRequest) -> ModerationDecision:
    client = SafetyClient()
    payload: Dict[str, Any] = client.detect_pii(request.text)
    spans = payload.get("spans") or payload.get("entities") or []
    redacted = redact_spans(request.text, spans)
    blocked = bool(payload.get("blocked", False)) or bool(spans)
    return ModerationDecision(
        allow=not blocked,
        category="unsafe_span_redaction",
        severity=1.0 if blocked else 0.0,
        redacted_text=redacted,
        rationale=payload.get("rationale") or "unsafe spans redacted",
        raw=payload,
    )
