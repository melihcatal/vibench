from __future__ import annotations

from typing import Iterable, List

from moderate_text import moderate_text
from safety_models import SafetyDecision, SafetyRequest


def moderate_batch(messages: Iterable[SafetyRequest]) -> List[SafetyDecision]:
    return [moderate_text(message) for message in messages]
