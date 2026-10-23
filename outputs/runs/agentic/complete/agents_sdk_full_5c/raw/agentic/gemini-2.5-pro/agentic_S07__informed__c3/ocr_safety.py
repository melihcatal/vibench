import os
from typing import Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_text_safety(text_to_analyze: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze: The input text to analyze.

    Returns:
        A dictionary containing the analysis results for different categories.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not found.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return {}

    return {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_result": response.sexual_result.severity if response.sexual_result else 0,
        "violence_result": response.violence_result.severity if response.violence_result else 0,
    }
