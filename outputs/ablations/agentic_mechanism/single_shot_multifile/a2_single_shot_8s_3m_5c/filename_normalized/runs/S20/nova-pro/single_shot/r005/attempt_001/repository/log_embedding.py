import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def embed_log_message(log_message):
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('TEXT_ANALYTICS_KEY')
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.extract_key_phrases(documents=[log_message])[0]
    return result.key_phrases

# Example usage:
# embed_log_message('Error occurred during user login')