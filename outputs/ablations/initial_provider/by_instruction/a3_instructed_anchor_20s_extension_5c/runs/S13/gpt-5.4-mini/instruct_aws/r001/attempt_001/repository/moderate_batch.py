from typing import Any, Dict, List

from moderate_text import moderate_text
from safety_models import BatchSafetyResult


def moderate_batch(messages: List[str], thresholds: Dict[str, Any] | None = None) -> BatchSafetyResult:
    decisions = [moderate_text(message, thresholds=thresholds) for message in messages]
    return BatchSafetyResult(decisions=decisions)
