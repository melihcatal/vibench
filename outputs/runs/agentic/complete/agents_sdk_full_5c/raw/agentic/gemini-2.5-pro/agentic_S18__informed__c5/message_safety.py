import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_safety(text_to_analyze: str):
    """
    Checks input text for harmful content using Azure AI Content Safety.

    Returns:
        A dictionary with the analysis results for different categories.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return {"error": str(e)}

    results = {}
    if response.hate_result:
        results["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        results["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        results["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        results["violence"] = {"severity": response.violence_result.severity}
        
    return results
