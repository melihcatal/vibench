import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def embed_log_message(log_message):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = client.extract_key_phrases(documents=[log_message])
    return result[0].key_phrases

log_message = 'This is a sample log message.'
print(embed_log_message(log_message))