from typing import Any, List, Optional

from moderate_text import moderate_text
from safety_models import RedactionResult, normalize_text


def redact_unsafe(text: Any, *, region: Optional[str] = None) -> RedactionResult:
    decision = moderate_text(text, region=region)
    source = normalize_text(text)
    spans: List[dict] = []
    if not decision.allowed and source:
        spans.append({"start": 0, "end": len(source), "label": "unsafe"})
        source = "[REDACTED]"
    return RedactionResult(text=source, spans=spans, provider=decision.provider)
