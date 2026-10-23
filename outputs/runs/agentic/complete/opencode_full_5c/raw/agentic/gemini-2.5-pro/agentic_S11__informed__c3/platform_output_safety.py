import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_content_safety(text_to_analyze: str):
    """
    Checks platform model output for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze: The text string to analyze.

    Returns:
        The analysis result from the Azure AI Content Safety service.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        raise

    return response
