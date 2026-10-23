from __future__ import annotations

from typing import Dict, Optional

from safety_client import build_thresholds
from safety_models import SafetyDecision, severity_map


def apply_safety_threshold(decision: SafetyDecision, thresholds: Optional[Dict[str, int]] = None) -> SafetyDecision:
    active = build_thresholds(thresholds)
    severities = severity_map(decision.categories)
    block_reasons = [
        category for category, severity in severities.items() if severity >= active.get(category, 99)
    ]
    decision.allowed = len(block_reasons) == 0
    decision.block_reasons = block_reasons
    decision.metadata["thresholds"] = active
    decision.metadata["provider"] = "Azure AI Content Safety"
    return decision
