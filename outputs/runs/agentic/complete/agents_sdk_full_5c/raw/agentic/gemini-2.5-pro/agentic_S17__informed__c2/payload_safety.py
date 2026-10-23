import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_payload_safety(text_payload: str) -> dict:
    """
    Checks a decrypted text payload for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

    request = AnalyzeTextOptions(text=text_payload)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP error during analysis: {e.message}"}


    results = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }

    return results
