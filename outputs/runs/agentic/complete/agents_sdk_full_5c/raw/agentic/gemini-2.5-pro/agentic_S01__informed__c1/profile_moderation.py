import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates user profile text using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
    
    request = AnalyzeTextOptions(text=profile_text)
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        raise RuntimeError(f"Content safety analysis failed: {e}")

    results = {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
    return results
