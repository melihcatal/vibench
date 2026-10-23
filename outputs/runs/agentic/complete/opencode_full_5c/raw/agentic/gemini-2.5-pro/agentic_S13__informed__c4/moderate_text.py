from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_safety_client
from safety_models import ModerationResponse, SafetyCategory as SafetyCategoryModel


def moderate_text(text: str) -> ModerationResponse:
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception:
        return ModerationResponse(success=False)

    result = {}
    if response.hate_result:
        result["hate"] = SafetyCategoryModel(
            category=TextCategory.HATE, severity=response.hate_result.severity
        )
    if response.self_harm_result:
        result["self_harm"] = SafetyCategoryModel(
            category=TextCategory.SELF_HARM, severity=response.self_harm_result.severity
        )
    if response.sexual_result:
        result["sexual"] = SafetyCategoryModel(
            category=TextCategory.SEXUAL, severity=response.sexual_result.severity
        )
    if response.violence_result:
        result["violence"] = SafetyCategoryModel(
            category=TextCategory.VIOLENCE, severity=response.violence_result.severity
        )

    return ModerationResponse(**result)
