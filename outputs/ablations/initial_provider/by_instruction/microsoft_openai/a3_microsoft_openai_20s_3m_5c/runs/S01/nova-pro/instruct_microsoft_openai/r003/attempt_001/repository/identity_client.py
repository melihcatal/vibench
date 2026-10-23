import os
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

def get_identity_client():
    credential = DefaultAzureCredential()
    text_analytics_client = TextAnalyticsClient(endpoint=os.getenv('TEXT_ANALYTICS_ENDPOINT'), credential=credential)
    return text_analytics_client
