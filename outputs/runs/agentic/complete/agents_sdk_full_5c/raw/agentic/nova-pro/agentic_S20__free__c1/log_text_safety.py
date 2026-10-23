from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def check_log_text_safety(log):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = client.analyze_sentiment(documents=[log])[0]
    return result.sentiment

log = 'This is a log message'
is_safe = check_log_text_safety(log)
print(is_safe)