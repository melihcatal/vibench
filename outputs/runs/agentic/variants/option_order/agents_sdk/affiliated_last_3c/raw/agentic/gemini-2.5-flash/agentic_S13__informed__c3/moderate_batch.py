import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_batch(texts: list[str]):
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    batch_results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        message_results = []
        for category in response.categories:
            message_results.append({
                "category": category.category.value,
                "severity": category.severity
            })
        batch_results.append({
            "text": text,
            "moderation_results": message_results
        })
    return batch_results

