from __future__ import annotations

from typing import Iterable, List

from moderate_text import moderate_text
from safety_models import ModerationBatchResult, ModerationItem


def moderate_batch(items: Iterable[ModerationItem]) -> ModerationBatchResult:
    results: List = []
    for item in items:
        results.append(moderate_text(item.text))
    return ModerationBatchResult(provider="Hive AI", results=results)
