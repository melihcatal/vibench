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


DEFAULT_THRESHOLDS = {
    "hate": 4,
    "sexual": 4,
    "self_harm": 3,
    "violence": 4,
}


def moderate_text(
    text: str, language: str | None = None, user_id: str | None = None
) -> SafetyResult:
    request = SafetyRequest(text=text, language=language, user_id=user_id)
    response = azure_post(DEFAULT_AZURE_SAFETY_PATH, request.to_azure_payload())
    categories = normalize_categories(response.get("categoriesAnalysis"))
    severity_map = {item.name: item.severity for item in categories}
    action = normalize_action(severity_map, DEFAULT_THRESHOLDS)
    return SafetyResult(
        action=action,
        categories=categories,
        provider=azure_content_safety_config()["provider"],
        raw=response,
    )
