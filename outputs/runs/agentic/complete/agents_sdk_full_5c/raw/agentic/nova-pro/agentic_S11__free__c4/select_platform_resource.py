import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def select_resource():
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client