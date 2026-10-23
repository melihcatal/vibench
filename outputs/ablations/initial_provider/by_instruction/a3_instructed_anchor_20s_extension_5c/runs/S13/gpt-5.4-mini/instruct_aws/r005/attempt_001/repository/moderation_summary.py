from typing import Iterable

from safety_models import SafetyDecision


def moderation_summary(decisions: Iterable[SafetyDecision]) -> str:
    items = list(decisions)
    allowed = sum(1 for d in items if d.allowed)
    blocked = len(items) - allowed
    return f"aws-bedrock moderation summary: allowed={allowed} blocked={blocked}"
