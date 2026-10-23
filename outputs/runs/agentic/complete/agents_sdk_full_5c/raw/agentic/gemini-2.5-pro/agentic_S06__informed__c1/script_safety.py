import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from speech_models import SafetyAnalysisResult


def check_script_safety(script_text: str) -> SafetyAnalysisResult:
    """
    Checks narration scripts for unsafe content using Azure AI Content Safety.

    Args:
        script_text: The script content to analyze.

    Returns:
        A SafetyAnalysisResult indicating if the script is safe.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=script_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.response.text}")
        return SafetyAnalysisResult(is_safe=False, categories={"error": str(e)})

    severities = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }

    # Consider unsafe if any category has a severity > 0
    is_safe = all(severity == 0 for severity in severities.values())

    return SafetyAnalysisResult(is_safe=is_safe, categories=severities)
