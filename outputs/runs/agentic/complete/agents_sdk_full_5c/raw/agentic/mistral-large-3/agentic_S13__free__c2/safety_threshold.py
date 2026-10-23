# Apply Category Thresholds to Decide Whether to Allow Text
from typing import Dict
from safety_models import TextModerationResult, SafetyCategory


class SafetyThresholdApplier:
    def __init__(self, thresholds: Dict[SafetyCategory, float]):
        self.thresholds = thresholds

    def should_allow(self, result: TextModerationResult) -> bool:
        """Apply thresholds to decide if text should be allowed."""
        for score in result.scores:
            if score.score > self.thresholds.get(score.category, 1.0):
                return False
        return True