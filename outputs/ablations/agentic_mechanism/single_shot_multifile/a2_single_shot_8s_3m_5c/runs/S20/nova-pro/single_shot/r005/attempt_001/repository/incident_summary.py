import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def summarize_error_logs(logs):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    summary = client.extract_key_phrases(documents=logs)
    return summary

# Example usage:
# logs = ['Error occurred during user login', 'User login failed due to incorrect password']
# summarize_error_logs(logs)