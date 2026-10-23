import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_vendor_text_safety(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    Returns a dictionary of moderation results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not found.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP response error: {e.message}"}

    results = {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
    return results
