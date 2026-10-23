from __future__ import annotations

from typing import Optional

from safety_client import AzureContentSafetyClient
from safety_models import SafetyModerationRequest


def redact_unsafe(text: str, client: Optional[AzureContentSafetyClient] = None) -> str:
    client = client or AzureContentSafetyClient()
    payload = client.redact(text)
    return str(payload.get("redactedText", text))


def flag_or_redact(text: str, redact: bool = True, client: Optional[AzureContentSafetyClient] = None):
    client = client or AzureContentSafetyClient()
    analysis = client.analyze_text(text)
    if redact and analysis.get("isBlocked", False):
        return redact_unsafe(text, client=client)
    return {"flagged": bool(analysis.get("isBlocked", False)), "text": text, "analysis": analysis}
