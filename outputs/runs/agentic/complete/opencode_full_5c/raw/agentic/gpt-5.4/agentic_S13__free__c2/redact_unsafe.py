from __future__ import annotations

import re

from safety_client import moderate_text_with_openai
from safety_models import SafetyDecision, flagged_categories


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> SafetyDecision:
    decision = moderate_text_with_openai(text)
    redacted_text = text
    if decision.flagged:
        redacted_text = re.sub(r"\S+", replacement, text)
        decision.action = "redact"
    decision.redacted_text = redacted_text
    decision.raw["flagged_categories"] = flagged_categories(decision)
    return decision
