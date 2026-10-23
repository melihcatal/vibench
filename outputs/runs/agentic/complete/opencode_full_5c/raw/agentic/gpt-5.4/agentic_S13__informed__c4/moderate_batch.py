from __future__ import annotations

from typing import Any

from safety_client import analyze_text, get_content_safety_client
from safety_models import BatchModerationResult, SafetyRequest, result_to_dict


def moderate_batch(messages: list[str], language: str | None = None) -> dict[str, Any]:
    client = get_content_safety_client()
    results = [
        analyze_text(SafetyRequest(text=message, language=language), client=client)
        for message in messages
    ]
    batch = BatchModerationResult(results=results)
    return {
        "provider": "azure-ai-content-safety",
        "results": [result_to_dict(item) for item in batch.results],
        "flagged_count": sum(1 for item in batch.results if item.flagged),
    }
