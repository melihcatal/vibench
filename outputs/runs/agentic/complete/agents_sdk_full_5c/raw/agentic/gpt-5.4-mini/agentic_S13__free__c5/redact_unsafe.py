from __future__ import annotations

from typing import List

from openai import OpenAI

from safety_client import get_client, get_config
from safety_models import RedactionResult, RedactionSpan


def redact_unsafe(text: str) -> RedactionResult:
    config = get_config()
    client: OpenAI = get_client(config.api_key)
    response = client.moderations.create(model=config.moderation_model, input=text)
    decision = response.results[0]
    spans: List[RedactionSpan] = []
    redacted = text
    if decision.flagged:
        redacted = "[REDACTED]"
        for category, flagged in (getattr(decision, "categories", {}) or {}).items():
            if flagged:
                spans.append(RedactionSpan(start=0, end=len(text), label=str(category)))
    return RedactionResult(redacted_text=redacted, spans=spans, model=config.moderation_model, raw={"provider": "openai"})
