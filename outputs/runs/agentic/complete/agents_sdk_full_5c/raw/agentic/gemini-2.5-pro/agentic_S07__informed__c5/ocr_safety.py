import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_safety(text_to_analyze: str):
    """
    Checks text for harmful content using Azure AI Content Safety.

    Args:
        text_to_analyze: The input text to analyze.

    Returns:
        The analysis result from the service.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

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
        return {
            "hate_result": response.hate_result,
            "self_harm_result": response.self_harm_result,
            "sexual_result": response.sexual_result,
            "violence_result": response.violence_result,
        }
    except HttpResponseError as e:
        print(f"Error checking text safety: {e}")
        raise
