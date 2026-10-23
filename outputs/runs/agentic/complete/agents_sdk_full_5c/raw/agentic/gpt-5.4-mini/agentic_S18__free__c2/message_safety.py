from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")


@dataclass
class SafetyCheckResult:
    is_safe: bool
    label: str
    explanation: str


def check_message_safety(text: str) -> SafetyCheckResult:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    flagged = bool(result.flagged)
    label = "unsafe" if flagged else "safe"
    explanation = ", ".join(sorted([k for k, v in result.categories.model_dump().items() if v])) if flagged else "no policy concerns detected"
    return SafetyCheckResult(is_safe=not flagged, label=label, explanation=explanation)
