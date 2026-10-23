import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from security_models import ContentSafetyRequest, ContentSafetyResult


def check_payload_safety(request: ContentSafetyRequest) -> ContentSafetyResult:
    """
    Checks a text payload for unsafe content using Azure AI Content Safety.

    Args:
        request: A ContentSafetyRequest object containing the text to analyze.

    Returns:
        A ContentSafetyResult indicating if the content is safe and details.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

    analyze_request = AnalyzeTextOptions(text=request.text)

    try:
        response = client.analyze_text(analyze_request)
    except HttpResponseError as e:
        return ContentSafetyResult(
            is_safe=False, details={"error": f"HTTP response error: {e.message}"}
        )

    details = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    # Consider unsafe if any category has a severity > 0
    is_safe = all(severity == 0 for severity in details.values())

    return ContentSafetyResult(is_safe=is_safe, details=details)
