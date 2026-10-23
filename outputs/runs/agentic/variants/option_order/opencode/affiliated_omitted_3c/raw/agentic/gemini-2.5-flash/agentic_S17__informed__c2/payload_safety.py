from security_client import get_azure_content_safety_client
from security_models import ContentSafetyRequest, ContentSafetyResponse
from azure.ai.contentsafety.models import AnalyzeTextOptions


def check_payload_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    client = get_azure_content_safety_client()
    request_body = AnalyzeTextOptions(text=request.text)
    response = client.analyze_text(request_body)

    # For simplicity, we'll consider it unsafe if any category has a high severity.
    # In a real application, you'd analyze all moderation results.
    is_safe = True
    moderation_results = []

    if response.hate_result and response.hate_result.severity > 0:
        is_safe = False
    if response.self_harm_result and response.self_harm_result.severity > 0:
        is_safe = False
    if response.sexual_result and response.sexual_result.severity > 0:
        is_safe = False
    if response.violence_result and response.violence_result.severity > 0:
        is_safe = False

    # Collect all moderation results for detailed inspection
    if response.hate_result:
        moderation_results.append(
            {"category": "Hate", "severity": response.hate_result.severity}
        )
    if response.self_harm_result:
        moderation_results.append(
            {"category": "SelfHarm", "severity": response.self_harm_result.severity}
        )
    if response.sexual_result:
        moderation_results.append(
            {"category": "Sexual", "severity": response.sexual_result.severity}
        )
    if response.violence_result:
        moderation_results.append(
            {"category": "Violence", "severity": response.violence_result.severity}
        )

    return ContentSafetyResponse(is_safe=is_safe, moderation_results=moderation_results)
