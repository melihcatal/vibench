import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_script_safety(text_to_analyze: str):
    """Checks narration scripts for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

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
        print("Analyze text failed.")
        raise e

    return {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_result": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_result": response.violence_result.severity
        if response.violence_result
        else 0,
    }
