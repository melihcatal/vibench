from safety_models import SafetyThresholdRequest, SafetyThresholdResponse
from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions


def safety_threshold(request: SafetyThresholdRequest) -> SafetyThresholdResponse:
    client = get_content_safety_client()
    request_body = AnalyzeTextOptions(text=request.text)
    response = client.analyze_text(request_body)

    allowed = True
    reasons = []

    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            for threshold_config in request.thresholds:
                if category_analysis.category.value == threshold_config.category:
                    if category_analysis.severity >= threshold_config.threshold:
                        allowed = False
                        reasons.append(
                            f"Content exceeded threshold for category '{category_analysis.category.value}' "
                            f"(severity: {category_analysis.severity}, threshold: {threshold_config.threshold})"
                        )

    return SafetyThresholdResponse(text=request.text, allowed=allowed, reasons=reasons)
