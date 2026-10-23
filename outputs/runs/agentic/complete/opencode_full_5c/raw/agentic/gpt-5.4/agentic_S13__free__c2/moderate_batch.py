from __future__ import annotations

from typing import Iterable, List

from safety_client import moderate_batch_with_openai
from safety_models import SafetyDecision


def moderate_batch(messages: Iterable[str]) -> List[SafetyDecision]:
    return moderate_batch_with_openai(messages)
