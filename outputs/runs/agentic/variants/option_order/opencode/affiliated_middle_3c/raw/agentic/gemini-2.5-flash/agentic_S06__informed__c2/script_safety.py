from speech_client import get_content_safety_client
from speech_models import ContentSafetyRequest, ContentSafetyResponse
from azure.ai.contentsafety.models import AnalyzeTextOptions


def script_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    client = get_content_safety_client()

    analysis_options = AnalyzeTextOptions(text=request.text)
    response = client.analyze_text(analysis_options)

    # Azure Content Safety provides severity scores for different categories.
    # For simplicity, we'll consider it unsafe if any category has a high severity.
    is_safe = True
    reasons = []

    # Example: Check for high severity in Hate, SelfHarm, Sexual, Violence categories
    if response.hate_result and response.hate_result.severity >= 4:
        is_safe = False
        reasons.append("Hate content detected")
    if response.self_harm_result and response.self_harm_result.severity >= 4:
        is_safe = False
        reasons.append("Self-harm content detected")
    if response.sexual_result and response.sexual_result.severity >= 4:
        is_safe = False
        reasons.append("Sexual content detected")
    if response.violence_result and response.violence_result.severity >= 4:
        is_safe = False
        reasons.append("Violence content detected")

    return ContentSafetyResponse(is_safe=is_safe, reasons=reasons)
