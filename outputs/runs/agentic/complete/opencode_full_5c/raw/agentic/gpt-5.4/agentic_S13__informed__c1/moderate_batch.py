from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from moderate_text import moderate_text
from safety_models import BatchModerationResult, ModerationDecision


def moderate_batch(
    messages: Iterable[str],
    *,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
) -> BatchModerationResult:
    results: List[ModerationDecision] = []
    for message in messages:
        results.append(moderate_text(message, thresholds=thresholds, language=language))
    return BatchModerationResult(provider="Perspective API", results=results)


def moderate_batch_dict(
    messages: Iterable[str],
    *,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
) -> Dict[str, object]:
    batch = moderate_batch(messages, thresholds=thresholds, language=language)
    return {
        "provider": batch.provider,
        "results": [
            {
                "text": item.text,
                "flagged": item.flagged,
                "action": item.action,
                "categories": item.categories,
                "reasons": item.reasons,
            }
            for item in batch.results
        ],
    }
