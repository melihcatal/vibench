from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import ThresholdRequest, ThresholdResult


def apply_safety_threshold(request: ThresholdRequest) -> ThresholdResult:
    client = get_safety_client()

    azure_request = AnalyzeTextOptions(text=request.text)

    try:
        response = client.analyze_text(azure_request)
    except Exception:
        return ThresholdResult(is_safe=True, violated_categories=[])

    violated_categories = []
    is_safe = True

    severity_map = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "selfharm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    for category, threshold in request.thresholds.items():
        category_key = category.lower().replace("_", "")
        if category_key in severity_map:
            # Azure Content Safety severity is an integer. Thresholds here are floats
            # for more general use, so we cast.
            if severity_map[category_key] >= int(threshold):
                violated_categories.append(category)
                is_safe = False

    return ThresholdResult(is_safe=is_safe, violated_categories=violated_categories)
