from safety_client import SafetyClient
from safety_models import SafetyDecision, SafetyTextRequest, normalize_text


def moderate_text(request: SafetyTextRequest) -> SafetyDecision:
    client = SafetyClient()
    text = normalize_text(request.text)
    result = client.analyze_text(text, categories=request.categories)
    categories = (
        result.get("categoriesAnalysis", {}) if isinstance(result, dict) else {}
    )
    score = max(categories.values()) if categories else 0.0
    allowed = score < 0.5
    reasons = (
        [item.get("category", "") for item in result.get("categoriesAnalysis", [])]
        if isinstance(result, dict)
        else []
    )
    return SafetyDecision(
        allowed=allowed,
        score=score,
        categories=categories if isinstance(categories, dict) else {},
        reasons=reasons,
    )
