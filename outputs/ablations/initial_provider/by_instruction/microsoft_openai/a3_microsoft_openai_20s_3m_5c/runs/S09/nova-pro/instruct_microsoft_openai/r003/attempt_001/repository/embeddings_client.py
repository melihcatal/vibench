import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def get_text_analytics_client():
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client