import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

def select_resource():
    return client
