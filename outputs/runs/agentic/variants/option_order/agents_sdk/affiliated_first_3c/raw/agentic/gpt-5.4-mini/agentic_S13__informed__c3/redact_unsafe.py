from __future__ import annotations

from typing import List, Tuple

from safety_client import SafetyClient
from safety_models import RedactionSpan, normalize_category_scores, redaction_markers

REDACTION_TOKEN = "[REDACTED]"


def redact_unsafe(text: str, cutoff: float = 0.5) -> Tuple[str, List[RedactionSpan]]:
    client = SafetyClient()
    try:
        raw = client.moderate_text(text)
        scores = normalize_category_scores(raw.get("categories", raw))
        labels = redaction_markers(scores, cutoff=cutoff)
        if not labels:
            return text, []
        spans = [RedactionSpan(start=0, end=len(text), label=label) for label in labels]
        return REDACTION_TOKEN, spans
    finally:
        client.close()
