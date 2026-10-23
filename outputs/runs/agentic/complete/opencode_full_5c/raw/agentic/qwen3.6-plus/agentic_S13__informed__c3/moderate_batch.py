from safety_models import (
    SafetyCategory,
    BatchSafetyRequest,
    BatchSafetyResult,
    BatchSafetyResponse,
    SafetyResponse,
    CategoryScore,
    SeverityLevel,
)
from safety_client import call_azure_content_safety_batch, parse_response


def moderate_batch(
    texts: list[str],
    categories: list[SafetyCategory] | None = None,
) -> BatchSafetyResponse:
    if categories is None:
        categories = list(SafetyCategory)

    raw_results = call_azure_content_safety_batch(texts, categories)

    results = []
    for idx, (text, raw) in enumerate(zip(texts, raw_results)):
        safety_response = parse_response(text, raw, categories)
        results.append(
            BatchSafetyResult(
                index=idx,
                text=text,
                response=safety_response,
            )
        )

    return BatchSafetyResponse(
        results=results,
        total_processed=len(results),
    )


def moderate_batch_decisions(
    texts: list[str],
    categories: list[SafetyCategory] | None = None,
) -> list[dict]:
    batch_response = moderate_batch(texts, categories)

    decisions = []
    for result in batch_response.results:
        resp = result.response
        decision = {
            "index": result.index,
            "text": result.text,
            "block_action": resp.block_action,
            "categories": [],
        }
        for score in resp.category_scores:
            decision["categories"].append(
                {
                    "category": score.category.value,
                    "severity": score.severity.name,
                    "score": score.raw_score,
                }
            )
        decisions.append(decision)

    return decisions
