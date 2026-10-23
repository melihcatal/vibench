import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_claim_text(text_to_moderate: str) -> dict:
    """
    Moderates free-text user claims using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_moderate)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        raise

    results = {}
    if response.hate_result:
        results['hate'] = {'severity': response.hate_result.severity}
    if response.self_harm_result:
        results['self_harm'] = {'severity': response.self_harm_result.severity}
    if response.sexual_result:
        results['sexual'] = {'severity': response.sexual_result.severity}
    if response.violence_result:
        results['violence'] = {'severity': response.violence_result.severity}
        
    return results
