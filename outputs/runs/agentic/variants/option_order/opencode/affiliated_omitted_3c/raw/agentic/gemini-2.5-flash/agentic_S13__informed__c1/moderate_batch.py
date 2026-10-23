from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os


def moderate_batch(texts: list[str]):
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = []
    for text in texts:
        request = {"text": text}
        response = client.analyze_text(request)
        results.append(response.to_dict())
    return results
