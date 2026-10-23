import os
from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse


class ModerateText:
    def __init__(self):
        self.client = SafetyClient()

    def score(self, user_text: str) -> SafetyResponse:
        payload = SafetyRequest(text=user_text)
        try:
            response = self.client.moderate(payload)
            return SafetyResponse(**response)
        except Exception as e:
            raise RuntimeError(f"Moderation failed: {e}")
