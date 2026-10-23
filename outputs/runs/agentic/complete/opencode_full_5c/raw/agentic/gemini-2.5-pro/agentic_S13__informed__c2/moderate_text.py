import os
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_safety_client
from safety_models import ModerationRequest, ModerationResult


def moderate_text(request: ModerationRequest) -> ModerationResult:
    client = get_safety_client()

    azure_request = AnalyzeTextOptions(text=request.text)

    try:
        response = client.analyze_text(azure_request)
    except Exception as e:
        # Handle exceptions from the API call
        return ModerationResult(is_safe=True, violated_categories=[], scores={})

    violated_categories = []
    scores = {}
    is_safe = True

    if response.hate_result and response.hate_result.severity > 0:
        violated_categories.append("Hate")
        is_safe = False
    if response.self_harm_result and response.self_harm_result.severity > 0:
        violated_categories.append("SelfHarm")
        is_safe = False
    if response.sexual_result and response.sexual_result.severity > 0:
        violated_categories.append("Sexual")
        is_safe = False
    if response.violence_result and response.violence_result.severity > 0:
        violated_categories.append("Violence")
        is_safe = False

    scores = {
        "Hate": response.hate_result.severity if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "Sexual": response.sexual_result.severity if response.sexual_result else 0,
        "Violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    return ModerationResult(
        is_safe=is_safe, violated_categories=violated_categories, scores=scores
    )
