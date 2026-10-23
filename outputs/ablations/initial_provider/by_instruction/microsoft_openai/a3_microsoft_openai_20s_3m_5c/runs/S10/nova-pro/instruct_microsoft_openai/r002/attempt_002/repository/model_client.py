import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def get_text_analytics_client():
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    key = os.getenv('AZURE_OPENAI_KEY')
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))