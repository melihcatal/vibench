import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def check_secret_label_safety(text: str) -> dict:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
        result = {
            "hate_result": response.hate_result.severity
            if response.hate_result
            else None,
            "self_harm_result": response.self_harm_result.severity
            if response.self_harm_result
            else None,
            "sexual_result": response.sexual_result.severity
            if response.sexual_result
            else None,
            "violence_result": response.violence_result.severity
            if response.violence_result
            else None,
        }
        return result
    except Exception as e:
        raise Exception(f"Error checking content safety: {e}")
