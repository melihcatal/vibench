from document_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_vendor_notes(text: str) -> dict:
    content_safety_client = get_azure_content_safety_client()

    request = AnalyzeTextOptions(text=text)
    response = content_safety_client.analyze_text(request)

    result = {
        "hate_result": {
            "severity": response.hate_result.severity if response.hate_result else None
        },
        "self_harm_result": {
            "severity": response.self_harm_result.severity
            if response.self_harm_result
            else None
        },
        "sexual_result": {
            "severity": response.sexual_result.severity
            if response.sexual_result
            else None
        },
        "violence_result": {
            "severity": response.violence_result.severity
            if response.violence_result
            else None
        },
    }
    return result
