import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_script_safety(text: str) -> dict:
    """
    Checks a narration script for unsafe content using Azure AI Content Safety.

    Args:
        text: The script text to analyze.

    Returns:
        A dictionary with content safety analysis results.
    """
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"Error analyzing text with Azure Content Safety: {e}")
        return {}

    return {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }
