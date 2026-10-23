from __future__ import annotations

from safety_client import analyze_text, get_azure_content_safety_config
from safety_models import ModerationResult, max_score, normalize_azure_categories


def moderate_text(text: str) -> dict:
    response_json = analyze_text(text)
    categories = normalize_azure_categories(response_json)
    result = ModerationResult(
        text=text,
        provider=get_azure_content_safety_config()["provider"],
        model="Azure AI Content Safety text:analyze",
        categories=categories,
        overall_score=max_score(categories),
        block=any(c.blocked or c.score >= 4 for c in categories),
        raw_response=response_json,
    )
    return result.to_dict()
