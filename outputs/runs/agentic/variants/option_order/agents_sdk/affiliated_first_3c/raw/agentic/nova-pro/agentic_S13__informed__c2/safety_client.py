import os
from azure.ai.contentsafety import ContentSafetyClient

def get_client():
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    return ContentSafetyClient(endpoint=endpoint, credential=key)