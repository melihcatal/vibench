import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from speech_models import SafetyCheckRequest, SafetyCheckResponse


def check_script_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Checks a script for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    analyze_request = AnalyzeTextOptions(
        text=request.text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(analyze_request)
    except HttpResponseError as e:
        return SafetyCheckResponse(is_safe=False, details={"error": str(e)})

    is_safe = all(category.severity == 0 for category in response.categories_analysis)

    details = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_severity": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_severity": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    return SafetyCheckResponse(is_safe=is_safe, details=details)
