from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def embed_log_message(log):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = client.extract_key_phrases([log])[0]
    return result.key_phrases

log = 'This is a log message'
embedding = embed_log_message(log)
print(embedding)