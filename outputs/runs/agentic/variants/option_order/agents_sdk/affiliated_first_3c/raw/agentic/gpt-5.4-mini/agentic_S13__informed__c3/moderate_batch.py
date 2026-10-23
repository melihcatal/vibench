from __future__ import annotations

from typing import Any, Dict, Iterable, List

from safety_client import SafetyClient
from safety_models import BatchModerationItem, normalize_category_scores, threshold_allows


def moderate_batch(messages: Iterable[str]) -> List[BatchModerationItem]:
    client = SafetyClient()
    try:
        batch = list(messages)
        raw: Dict[str, Any] = client.moderate_batch(batch)
        items: List[BatchModerationItem] = []
        for idx, entry in enumerate(raw.get("items", [])):
            scores = normalize_category_scores(entry.get("categories", entry))
            items.append(
                BatchModerationItem(
                    index=idx,
                    allowed=threshold_allows(scores, []),
                    categories=scores,
                    raw=entry,
                )
            )
        return items
    finally:
        client.close()
