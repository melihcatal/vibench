from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_client(config):
    return ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))