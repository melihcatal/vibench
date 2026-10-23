import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_for_unsafe_content(text_to_analyze: str) -> dict:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze: The text string to analyze.

    Returns:
        A dictionary with the analysis results for different categories.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP response error: {e.message}"}

    results = {
        "hate": TextCategory.HATE,
        "self_harm": TextCategory.SELF_HARM,
        "sexual": TextCategory.SEXUAL,
        "violence": TextCategory.VIOLENCE,
    }

    return {
        category_name: {
            "severity": result.severity
        }
        for category_name, result in zip(
            results.keys(), response.categories_analysis
        )
    }
