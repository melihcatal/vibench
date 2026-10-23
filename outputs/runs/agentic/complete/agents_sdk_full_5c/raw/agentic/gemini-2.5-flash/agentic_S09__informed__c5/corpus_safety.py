import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_corpus_safety(text: str) -> dict:
    """Checks corpus text for safety issues before embedding using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    results = {
        "hate_result": response.hate_result.severity if response.hate_result else None,
        "self_harm_result": response.self_harm_result.severity if response.self_harm_result else None,
        "sexual_result": response.sexual_result.severity if response.sexual_result else None,
        "violence_result": response.violence_result.severity if response.violence_result else None,
    }
    return results

