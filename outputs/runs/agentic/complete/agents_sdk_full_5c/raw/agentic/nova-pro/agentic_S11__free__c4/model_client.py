import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def get_client():
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)