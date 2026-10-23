from typing import Dict
from dataclasses import dataclass
from safety_client import SafetyClient


class ThresholdPolicy:
    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds

    def allow(self, response: Dict) -> bool:
        for category, limit in self.thresholds.items():
            if response.get(category, 0.0) > limit:
                return False
        return True


def apply_thresholds(text: str, policy: ThresholdPolicy) -> bool:
    """Apply category thresholds to decide whether to allow the supplied text.
    Returns True if allowed, False otherwise.
    """
    client = SafetyClient()
    response = client.moderate(text)
    return policy.allow(response)
