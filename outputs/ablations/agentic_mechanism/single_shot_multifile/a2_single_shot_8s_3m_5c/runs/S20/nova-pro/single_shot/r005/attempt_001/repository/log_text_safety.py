import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def check_log_text_safety(log_text):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.analyze_sentiment(documents=[log_text])[0]
    return result.sentiment

# Example usage:
# check_log_text_safety('Error occurred during user login')