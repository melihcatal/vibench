import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_text_safety(text_to_analyze: str):
    """
    Analyzes text for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze (str): The input text to analyze.

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
            "hate": response.categories_analysis[0].severity,
            "self_harm": response.categories_analysis[1].severity,
            "sexual": response.categories_analysis[2].severity,
            "violence": response.categories_analysis[3].severity,
        }

    except Exception as e:
        print(f"Error checking text safety: {e}")
        return None
