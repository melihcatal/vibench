import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def payload_safety(text: str, endpoint: str = None, key: str = None) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze for unsafe content.
        endpoint: Azure AI Content Safety endpoint. Defaults to AZURE_CONTENT_SAFETY_ENDPOINT env var.
        key: Azure AI Content Safety key. Defaults to AZURE_CONTENT_SAFETY_KEY env var.

    Returns:
        Dictionary containing safety results, provider, and success status.
    """
    endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        return {
            "error": "Azure Content Safety endpoint and key are required",
            "provider": "azure_ai_content_safety",
            "success": False,
        }

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )

        response = client.analyze_text(request)

        return {
            "hate_severity": response.hate_result.severity,
            "self_harm_severity": response.self_harm_result.severity,
            "sexual_severity": response.sexual_result.severity,
            "violence_severity": response.violence_result.severity,
            "is_safe": all(
                result.severity == 0
                for result in [
                    response.hate_result,
                    response.self_harm_result,
                    response.sexual_result,
                    response.violence_result,
                ]
            ),
            "provider": "azure_ai_content_safety",
            "success": True,
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "azure_ai_content_safety",
            "success": False,
        }
