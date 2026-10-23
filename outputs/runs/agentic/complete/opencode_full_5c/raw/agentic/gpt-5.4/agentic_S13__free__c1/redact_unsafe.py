from __future__ import annotations

import re
from typing import List

from moderate_text import moderate_text
from safety_models import SafetyDecision


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> SafetyDecision:
    decision = moderate_text(text)
    blocked_names: List[str] = [
        item.name for item in decision.categories if item.blocked
    ]
    redacted_text = text
    spans = []
    for name in blocked_names:
        token = name.replace("_", " ")
        pattern = re.compile(re.escape(token), re.IGNORECASE)
        for match in pattern.finditer(redacted_text):
            spans.append({"label": name, "start": match.start(), "end": match.end()})
        redacted_text = pattern.sub(replacement, redacted_text)
    action = "redact" if spans else decision.action
    return SafetyDecision(
        provider="Hive AI",
        allowed=decision.allowed and not spans,
        action=action,
        categories=decision.categories,
        redacted_text=redacted_text,
        flagged_spans=spans,
        raw=decision.raw,
    )
