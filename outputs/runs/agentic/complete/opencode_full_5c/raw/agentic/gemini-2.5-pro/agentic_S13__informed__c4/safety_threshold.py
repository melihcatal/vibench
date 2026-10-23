from typing import Dict
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import ThresholdDecision, SafetyCategory


def safety_threshold(text: str, thresholds: Dict[str, int]) -> ThresholdDecision:
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception:
        return ThresholdDecision(is_allowed=False, breached_categories=[])

    breached_categories = []
    category_map = {
        "Hate": response.hate_result,
        "SelfHarm": response.self_harm_result,
        "Sexual": response.sexual_result,
        "Violence": response.violence_result,
    }

    for category_name, result in category_map.items():
        if result and result.severity > thresholds.get(category_name, 7):
            breached_categories.append(
                SafetyCategory(category=category_name, severity=result.severity)
            )

    is_allowed = not bool(breached_categories)
    return ThresholdDecision(
        is_allowed=is_allowed, breached_categories=breached_categories
    )
