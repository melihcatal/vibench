import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def get_text_analytics_client():
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)