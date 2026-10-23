from typing import List

from safety_models import BatchModerationResult, ModerationDecision, ModerationRequest
from moderate_text import moderate_text


def moderate_batch(messages: List[ModerationRequest]) -> BatchModerationResult:
    results = [moderate_text(message) for message in messages]
    return BatchModerationResult(results=results)
