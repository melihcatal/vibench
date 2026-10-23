from __future__ import annotations

from typing import Iterable, List, Optional

from moderate_text import moderate_text
from safety_models import BatchModerationResult, SafetyDecision


def moderate_batch(messages: Iterable[str], blocklist_name: Optional[str] = None) -> BatchModerationResult:
    decisions: List[SafetyDecision] = [
        moderate_text(text=message, blocklist_name=blocklist_name) for message in messages
    ]
    return BatchModerationResult(decisions=decisions)
