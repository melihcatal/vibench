import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_profile_text(text_to_moderate: str) -> dict:
    """
    Moderates profile text using Azure AI Content Safety.
    """
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_moderate,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            Text.Category.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        # Handle exceptions
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
