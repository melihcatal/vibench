from typing import Any, Iterable, List, Optional

from moderate_text import moderate_text
from safety_models import BatchSafetyDecision, SafetyDecision


def moderate_batch(messages: Iterable[Any], *, region: Optional[str] = None) -> BatchSafetyDecision:
    decisions: List[SafetyDecision] = [moderate_text(message, region=region) for message in messages]
    return BatchSafetyDecision(decisions=decisions, provider="aws-bedrock")
