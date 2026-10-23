from __future__ import annotations

from typing import Iterable, List, Optional

from safety_client import AzureContentSafetyClient
from safety_models import ModerationBatchItem, ModerationDecision, SafetyModerationRequest, chunk_texts
from moderate_text import moderate_text, to_decision


def moderate_batch(texts: Iterable[str], client: Optional[AzureContentSafetyClient] = None) -> List[ModerationBatchItem]:
    client = client or AzureContentSafetyClient()
    items: List[ModerationBatchItem] = []
    for index, text in enumerate(chunk_texts(texts)):
        result = moderate_text(SafetyModerationRequest(text=text), client=client)
        items.append(ModerationBatchItem(index=index, text=text, decision=to_decision(result)))
    return items


def batch_summary(items: List[ModerationBatchItem]) -> dict:
    blocked = sum(1 for item in items if not item.decision.allowed)
    return {"count": len(items), "blocked": blocked, "allowed": len(items) - blocked}
