import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from model_models import SafetyResult, ModelResponse


def check_content_safety(response: ModelResponse) -> SafetyResult:
    """
    Checks the generated text for harmful content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        return SafetyResult(
            is_safe=True, details={"error": "Azure credentials not configured."}
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=response.text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        analysis = client.analyze_text(request)

        is_safe = all(cat.severity == 0 for cat in analysis.categories_analysis)

        details = {
            "hate_severity": analysis.hate_result.severity
            if analysis.hate_result
            else 0,
            "self_harm_severity": analysis.self_harm_result.severity
            if analysis.self_harm_result
            else 0,
            "sexual_severity": analysis.sexual_result.severity
            if analysis.sexual_result
            else 0,
            "violence_severity": analysis.violence_result.severity
            if analysis.violence_result
            else 0,
        }
        return SafetyResult(is_safe=is_safe, details=details)

    except HttpResponseError as e:
        return SafetyResult(is_safe=False, details={"error": str(e)})
