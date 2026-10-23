import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def summarize_error_logs(logs):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    documents = [log['event'] for log in logs]
    response = client.extract_key_phrases(documents=documents)
    key_phrases = [doc.key_phrases for doc in response if not doc.is_error]
    return key_phrases

logs = [{'event': 'Error occurred during user login'}, {'event': 'User login failed due to incorrect password'}]
print(summarize_error_logs(logs))