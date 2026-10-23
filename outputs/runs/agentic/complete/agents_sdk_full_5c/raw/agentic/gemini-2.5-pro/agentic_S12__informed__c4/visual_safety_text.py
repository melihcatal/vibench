import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

from vision_models import Label

def check_text_safety(labels: list[Label]) -> dict:
    """
    Checks a list of text labels for harmful content using Azure AI Content Safety.

    Args:
        labels: A list of Label objects from a vision analysis.

    Returns:
        A dictionary with content safety analysis results.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    text_to_check = ", ".join([label.description for label in labels])

    if not text_to_check.strip():
        return {"status": "no text to analyze"}
        
    request = AnalyzeTextOptions(text=text_to_check)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return {}

    return {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }
