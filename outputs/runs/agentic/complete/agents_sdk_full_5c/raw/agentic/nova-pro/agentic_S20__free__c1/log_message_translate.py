from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def translate_log_message(log, to_language):
    endpoint = os.environ['TEXT_ANALYTICS_ENDPOINT']
    key = os.environ['TEXT_ANALYTICS_KEY']
    client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = client.translate(log, to_language)[0]
    return result.translations[0].text

log = 'This is a log message'
translated_log = translate_log_message(log, 'es')
print(translated_log)