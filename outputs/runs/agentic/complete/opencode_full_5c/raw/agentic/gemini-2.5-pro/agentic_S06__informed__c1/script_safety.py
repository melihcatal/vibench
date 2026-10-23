import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions


def check_script_safety(text_to_analyze: str):
    """
    Checks narration scripts for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze: The script text to analyze.

    Returns:
        The analysis response from the service.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
        return response
    except HttpResponseError as e:
        print(f"Error analyzing text: {e}")
        raise
