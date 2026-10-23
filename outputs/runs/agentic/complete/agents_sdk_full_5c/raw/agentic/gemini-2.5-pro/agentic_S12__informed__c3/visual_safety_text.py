
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_safety(text_to_analyze: str) -> dict:
    """
    Checks generated text for safety concerns using Azure AI Content Safety.
    """
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text_to_analyze)
    
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        raise e

    return {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
