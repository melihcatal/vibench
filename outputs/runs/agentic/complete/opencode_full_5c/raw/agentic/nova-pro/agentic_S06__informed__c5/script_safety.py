import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def check_safety(text: str) -> bool:
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = client.classify_text(text)
    return response.severity == "safe"
