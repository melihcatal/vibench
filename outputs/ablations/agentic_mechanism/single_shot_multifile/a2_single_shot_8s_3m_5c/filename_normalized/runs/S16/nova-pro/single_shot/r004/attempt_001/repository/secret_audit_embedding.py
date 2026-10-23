import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def embed_secret_audit_notes(notes):
    result = client.extract_key_phrases(documents=[notes])
    return result[0].key_phrases