import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_profile_text(text_to_moderate: str) -> dict:
    """
    Moderates user profile text using Azure AI Content Safety.

    Args:
        text_to_moderate: The text from the user's profile.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_moderate, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        raise

    results = {}
    if response.hate_result:
        results['hate'] = response.hate_result.severity
    if response.self_harm_result:
        results['self_harm'] = response.self_harm_result.severity
    if response.sexual_result:
        results['sexual'] = response.sexual_result.severity
    if response.violence_result:
        results['violence'] = response.violence_result.severity

    return results
