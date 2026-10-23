from typing import List

from safety_client import configure_client
from safety_models import BatchModerationResult, ModerationDecision, ModerationRequest
from moderate_text import moderate_text


def moderate_batch(requests: List[ModerationRequest]) -> BatchModerationResult:
    configure_client()
    decisions = [moderate_text(req) for req in requests]
    return BatchModerationResult(decisions=decisions)
