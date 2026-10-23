from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def create_client(endpoint, api_key):
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))