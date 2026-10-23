from __future__ import annotations

from safety_client import (
    DEFAULT_AZURE_SAFETY_PATH,
    azure_content_safety_config,
    azure_post,
)
from safety_models import (
    SafetyRequest,
    SafetyResult,
    normalize_action,
    normalize_categories,
)


REDACTION_TOKEN = "[UNSAFE]"


def redact_unsafe(text: str, language: str | None = None) -> SafetyResult:
    request = SafetyRequest(text=text, language=language)
    response = azure_post(DEFAULT_AZURE_SAFETY_PATH, request.to_azure_payload())
    categories = normalize_categories(response.get("categoriesAnalysis"))
    severity_map = {item.name: item.severity for item in categories}
    action = normalize_action(
        severity_map, {"hate": 2, "sexual": 2, "self_harm": 2, "violence": 2}
    )
    redacted_text = text if action == "allow" else REDACTION_TOKEN
    return SafetyResult(
        action=action,
        categories=categories,
        provider=azure_content_safety_config()["provider"],
        raw=response,
        redacted_text=redacted_text,
    )
