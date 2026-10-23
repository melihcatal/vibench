import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def check_vendor_text_safety(text):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.analyze_sentiment(documents=[text])[0]
    return result.sentiment