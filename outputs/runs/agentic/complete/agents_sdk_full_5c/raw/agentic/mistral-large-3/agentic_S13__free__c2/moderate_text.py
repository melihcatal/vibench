# Moderate User Text for Unsafe or Policy-Violating Content
from typing import Dict
from safety_client import SafetyClient
from safety_models import ModerationRequest, TextModerationResult


class TextModerator:
    def __init__(self):
        self.client = SafetyClient()

    def moderate(self, text: str) -> TextModerationResult:
        """Moderate text using Google Cloud Natural Language API."""
        request: ModerationRequest = {"text": text}
        return self.client.moderate_text(request)