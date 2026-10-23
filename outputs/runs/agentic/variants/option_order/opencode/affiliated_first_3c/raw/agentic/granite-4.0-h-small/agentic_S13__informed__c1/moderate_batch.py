import os
from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse


class ModerateBatch:
    def __init__(self):
        self.client = SafetyClient()

    def moderate_batch(self, messages: list[str]) -> list[SafetyResponse]:
        payload = [SafetyRequest(text=msg) for msg in messages]
        try:
            batch = self.client.moderate_batch(payload)
            return [SafetyResponse(**item) for item in batch]
        except Exception as e:
            raise RuntimeError(f"Batch moderation failed: {e}")
