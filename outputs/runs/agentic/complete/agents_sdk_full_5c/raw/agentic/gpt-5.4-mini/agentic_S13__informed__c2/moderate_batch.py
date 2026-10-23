from __future__ import annotations

from typing import Iterable, List

from safety_client import SafetyClient
from safety_models import BatchSafetyResponse, TextSafetyRequest


client = SafetyClient()


def moderate_batch(messages: Iterable[str]) -> BatchSafetyResponse:
    decisions = []
    for message in messages:
        decision = client.analyze_text(TextSafetyRequest(text=message, categories=["Hate", "SelfHarm", "Sexual", "Violence"]))
        decisions.append(decision)
    return BatchSafetyResponse(decisions=decisions)
