from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_safety_client(endpoint, api_key):
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))