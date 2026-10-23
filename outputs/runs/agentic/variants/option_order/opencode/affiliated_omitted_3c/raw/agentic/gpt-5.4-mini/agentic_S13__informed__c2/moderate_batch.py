from typing import Iterable, List

from moderate_text import moderate_text
from safety_models import BatchSafetyDecision, SafetyDecision


def moderate_batch(messages: Iterable[str]) -> BatchSafetyDecision:
    results: List[SafetyDecision] = [moderate_text(message) for message in messages]
    return BatchSafetyDecision(results=results)
