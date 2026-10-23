from typing import Dict
from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_contentsafety_client
from safety_models import SafetyThresholdResponse


def apply_safety_thresholds(
    text: str, thresholds: Dict[str, int]
) -> SafetyThresholdResponse:
    client = get_contentsafety_client()

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"An error occurred: {e}")
        return SafetyThresholdResponse(is_safe=True, violated_categories=[])

    violated_categories = []
    is_safe = True

    for category_analysis in response.categories_analysis:
        category_name = str(category_analysis.category)
        severity = category_analysis.severity

        if (
            category_name in thresholds
            and severity is not None
            and severity >= thresholds[category_name]
        ):
            violated_categories.append(category_name)
            is_safe = False

    return SafetyThresholdResponse(
        is_safe=is_safe, violated_categories=violated_categories
    )
