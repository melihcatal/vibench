import os
from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse


class SafetyThreshold:
    def __init__(self, thresholds: dict):
        self.client = SafetyClient()
        self.thresholds = thresholds

    def apply(self, response: SafetyResponse) -> bool:
        for category, limit in self.thresholds.items():
            if getattr(response, category, 0) > limit:
                return False
        return True
