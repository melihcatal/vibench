import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_transcript_text(text: str) -> dict:
    """
    Moderates transcript text using Azure AI Content Safety.

    Args:
        text: The text content to moderate.

    Returns:
        A dictionary containing moderation results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        moderation_results = {
            "hate": response.hate_result.severity if response.hate_result else None,
            "self_harm": response.self_harm_result.severity if response.self_harm_result else None,
            "sexual": response.sexual_result.severity if response.sexual_result else None,
            "violence": response.violence_result.severity if response.violence_result else None,
        }
        return moderation_results
    except Exception as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        return {"error": str(e)}
