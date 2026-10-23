from __future__ import annotations

from safety_client import AzureContentSafetyClient
from safety_models import ModerationDecision, normalize_azure_categories


DEFAULT_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


def moderate_text(text: str) -> ModerationDecision:
    client = AzureContentSafetyClient()
    response = client.analyze_text(text, categories=DEFAULT_CATEGORIES)
    categories = normalize_azure_categories(response.get("categoriesAnalysis", []))
    allowed = not any(item.blocked or item.score >= 4 for item in categories)
    return ModerationDecision(
        text=text,
        allowed=allowed,
        categories=categories,
        provider="azure_ai_content_safety",
        reason="azure contentsafety/text:analyze",
    )
