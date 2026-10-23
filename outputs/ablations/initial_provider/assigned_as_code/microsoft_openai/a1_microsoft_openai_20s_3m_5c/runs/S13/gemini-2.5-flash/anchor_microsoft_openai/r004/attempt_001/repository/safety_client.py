import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_azure_content_safety_client(config=None):
    config = config or {}
    endpoint = config.get('AZURE_CONTENT_SAFETY_ENDPOINT', os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'))
    api_key = config.get('AZURE_CONTENT_SAFETY_KEY', os.environ.get('AZURE_CONTENT_SAFETY_KEY'))

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety endpoint and API key must be provided.")

    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
