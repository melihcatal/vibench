import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_text_safety(text_to_check: str):
    """
    Checks user-generated text for harmful content using Azure AI Content Safety.

    Args:
        text_to_check: The text string to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not configured.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
    
    request = AnalyzeTextOptions(text=text_to_check)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.response.text}")
        return None

    # Process and return the results in a simplified format
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
