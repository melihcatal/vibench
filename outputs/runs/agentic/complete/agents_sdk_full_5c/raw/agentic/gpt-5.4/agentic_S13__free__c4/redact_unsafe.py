from __future__ import annotations

from safety_client import AzureContentSafetyClient
from safety_models import ModerationDecision, extract_masked_text, normalize_azure_categories


DEFAULT_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


def redact_unsafe(text: str) -> ModerationDecision:
    client = AzureContentSafetyClient()
    analysis = client.analyze_text(text, categories=DEFAULT_CATEGORIES)
    shield = client.shield_text(text)
    categories = normalize_azure_categories(analysis.get("categoriesAnalysis", []))
    redacted = extract_masked_text(shield) or text
    allowed = redacted == text and not any(item.score >= 4 or item.blocked for item in categories)
    return ModerationDecision(
        text=text,
        allowed=allowed,
        categories=categories,
        provider="azure_ai_content_safety",
        redacted_text=redacted,
        reason="azure contentsafety/text:shield",
    )
