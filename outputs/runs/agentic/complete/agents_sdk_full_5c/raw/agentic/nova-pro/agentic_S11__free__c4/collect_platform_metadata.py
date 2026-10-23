import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def collect_metadata(text):
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.analyze_sentiment(documents=[text])
    return result[0].__dict__