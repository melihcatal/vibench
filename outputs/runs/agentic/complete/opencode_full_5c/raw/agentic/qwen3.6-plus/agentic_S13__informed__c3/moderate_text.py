from safety_models import SafetyRequest, SafetyResponse, SafetyCategory
from safety_client import call_azure_content_safety


def moderate_text(
    text: str,
    categories: list[SafetyCategory] | None = None,
) -> SafetyResponse:
    if categories is None:
        categories = list(SafetyCategory)

    request = SafetyRequest(text=text, categories=categories)
    response = call_azure_content_safety(request)
    return response


def moderate_text_with_flags(
    text: str,
    categories: list[SafetyCategory] | None = None,
) -> dict:
    response = moderate_text(text, categories)

    flagged = []
    for score in response.category_scores:
        if score.severity.value >= 2:
            flagged.append(
                {
                    "category": score.category.value,
                    "severity": score.severity.name,
                    "score": score.raw_score,
                }
            )

    return {
        "text": text,
        "flagged": flagged,
        "block_action": response.block_action,
        "category_scores": [
            {
                "category": s.category.value,
                "severity": s.severity.name,
                "score": s.raw_score,
            }
            for s in response.category_scores
        ],
    }
