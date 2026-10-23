from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def summarize_error_logs(logs):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    summaries = client.extract_key_phrases(logs)
    return summaries

logs = ['This is an error log', 'Another error log']
summaries = summarize_error_logs(logs)
for summary in summaries:
    print(summary.key_phrases)