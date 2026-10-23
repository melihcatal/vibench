from typing import List

from moderate_text import moderate_text
from safety_models import BatchSafetyDecision


def moderate_batch(messages: List[str]) -> BatchSafetyDecision:
    return BatchSafetyDecision(decisions=[moderate_text(message) for message in messages])
