from __future__ import annotations

from typing import Iterable, List

from safety_client import analyze_text, get_azure_content_safety_config
from safety_models import BatchModerationResult, ModerationResult, max_score, normalize_azure_categories


def moderate_batch(messages: Iterable[str]) -> dict:
    provider = get_azure_content_safety_config()["provider"]
    results: List[ModerationResult] = []
    for text in messages:
        response_json = analyze_text(text)
        categories = normalize_azure_categories(response_json)
        results.append(
            ModerationResult(
                text=text,
                provider=provider,
                model="Azure AI Content Safety text:analyze",
                categories=categories,
                overall_score=max_score(categories),
                block=any(c.blocked or c.score >= 4 for c in categories),
                raw_response=response_json,
            )
        )
    return BatchModerationResult(results=results).to_dict()
