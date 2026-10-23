import os
from typing import List
from observability_models import SafetyCheck
from observability_client import get_safety_client


def check_safety(messages: List[str]) -> List[SafetyCheck]:
    """Check a list of log messages for unsafe content using Azure AI Content Safety.

    The concrete provider used is Azure AI Content Safety (REST) via azure-ai-contentsafety.
    """
    safety_client = get_safety_client()
    # Azure Content Safety expects batches of up to 100 texts – chunk if needed
    batch_size = 100
    results = []
    for i in range(0, len(messages), batch_size):
        batch = messages[i : i + batch_size]
        resp = safety_client.analyze_content(batch)
        results.extend(resp.reports)
    return results


# Helper to create the Azure client – uses AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
def get_safety_client():
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    credential = AzureKeyCredential(key)
    return ContentSafetyClient(endpoint=endpoint, credential=credential)
