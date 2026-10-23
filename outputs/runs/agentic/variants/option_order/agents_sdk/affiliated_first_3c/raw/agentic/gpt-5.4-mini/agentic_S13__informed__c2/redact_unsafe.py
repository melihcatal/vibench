from __future__ import annotations

from typing import Any, Dict, List

from safety_client import ContentSafetyClient
from safety_models import RedactionSpan


def redact_unsafe(text: str) -> Dict[str, Any]:
    client = ContentSafetyClient()
    result = client.moderate_text(text)
    spans: List[RedactionSpan] = []
    for item in result.get("spans", []):
        spans.append(RedactionSpan(start=int(item.get("start", 0)), end=int(item.get("end", 0)), label=str(item.get("category", "unsafe"))))
    redacted = text
    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        redacted = redacted[: span.start] + "[REDACTED]" + redacted[span.end :]
    return {"redacted_text": redacted, "spans": [span.__dict__ for span in spans], "raw": result}
