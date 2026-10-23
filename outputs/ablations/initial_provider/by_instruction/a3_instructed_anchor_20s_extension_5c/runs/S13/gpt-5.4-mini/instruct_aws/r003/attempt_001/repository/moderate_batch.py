from typing import List

from moderate_text import moderate_text
from safety_models import SafetyBatchDecision, normalize_texts


def moderate_batch(messages: List[str]) -> SafetyBatchDecision:
    return SafetyBatchDecision(items=[moderate_text(text) for text in normalize_texts(messages)])
