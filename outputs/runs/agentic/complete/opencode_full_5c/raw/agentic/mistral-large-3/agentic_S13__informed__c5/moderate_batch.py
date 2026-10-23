from typing import List
from safety_client import WatsonXGuardrailsClient
from safety_models import BatchModerationResult, ModerationResult


def moderate_batch(texts: List[str]) -> BatchModerationResult:
    """Moderate a batch of user messages using WatsonX Guardrails."""
    client = WatsonXGuardrailsClient()
    results = client.moderate_batch(texts)

    moderation_results = [
        ModerationResult(
            is_safe=result["is_safe"],
            score=result["score"],
            categories=result["categories"],
            flagged_reason="HAP detection" if not result["is_safe"] else "",
        )
        for result in results
    ]

    return BatchModerationResult(results=moderation_results)
