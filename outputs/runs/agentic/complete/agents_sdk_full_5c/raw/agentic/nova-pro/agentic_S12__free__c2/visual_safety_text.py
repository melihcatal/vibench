import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextBlocklist, TextBlocklistItem, TextBlocklistOperation
from azure.core.credentials import AzureKeyCredential

def check_text_safety(text):
    endpoint = os.getenv('CONTENTSAFETY_ENDPOINT')
    key = os.getenv('CONTENTSAFETY_KEY')
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    response = client.classify_text(text)
    return response.categories