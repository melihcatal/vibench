import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_user_claim(text_claim: str) -> dict:
    """
    Moderates a free-text user profile claim using Azure Content Safety.

    Args:
        text_claim (str): The text to be analyzed (e.g., a user's bio or display name).

    Returns:
        dict: A dictionary containing the moderation results.
    """
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not key or not endpoint:
        raise ValueError("Azure Content Safety credentials are not configured.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_claim)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.message}")
        raise

    results = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }

    return results
