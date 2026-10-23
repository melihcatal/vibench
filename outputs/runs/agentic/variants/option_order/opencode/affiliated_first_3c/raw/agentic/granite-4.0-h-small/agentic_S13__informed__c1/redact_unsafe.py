import os
from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse


class RedactUnsafe:
    def __init__(self):
        self.client = SafetyClient()

    def redact(self, text: str) -> str:
        payload = SafetyRequest(text=text)
        try:
            result = self.client.redact_unsafe(payload)
            return result.redacted_text
        except Exception as e:
            raise RuntimeError(f"Redaction failed: {e}")
