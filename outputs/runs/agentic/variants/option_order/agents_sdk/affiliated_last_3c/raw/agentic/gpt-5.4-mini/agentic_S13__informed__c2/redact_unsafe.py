from __future__ import annotations

from typing import List

from safety_client import get_client
from safety_models import ModerationRequest


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> str:
    decision = get_client().moderate(ModerationRequest(text=text))
    if not decision.flagged:
        return text
    return replacement if text.strip() else text
