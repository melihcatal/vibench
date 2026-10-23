import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def record_text_safety(text_to_analyze: str):
    """
    Checks user-generated document fields for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_analyze,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return None

    return {
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
