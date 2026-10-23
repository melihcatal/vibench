import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_safety(text: str) -> dict:
    """Checks prompts and generated text for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
        ],
    )

    try:
        response = client.analyze_text(request)
        result = {
            "hate_severity": response.hate_result.severity
            if response.hate_result
            else 0,
            "violence_severity": response.violence_result.severity
            if response.violence_result
            else 0,
            "self_harm_severity": response.self_harm_result.severity
            if response.self_harm_result
            else 0,
            "sexual_severity": response.sexual_result.severity
            if response.sexual_result
            else 0,
        }
        return result
    except Exception as e:
        return {"error": str(e)}
