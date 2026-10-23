from __future__ import annotations

from safety_client import moderate_text_with_openai
from safety_models import SafetyDecision


def moderate_text(text: str) -> SafetyDecision:
    return moderate_text_with_openai(text)
