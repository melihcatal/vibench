import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextBlocklistScreen, TextBlocklistItem
from azure.core.credentials import AzureKeyCredential

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

client = ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))

def safety_threshold(text):
    response = client.analyze_text(text)
    return response.hate_result.severity >= 2
