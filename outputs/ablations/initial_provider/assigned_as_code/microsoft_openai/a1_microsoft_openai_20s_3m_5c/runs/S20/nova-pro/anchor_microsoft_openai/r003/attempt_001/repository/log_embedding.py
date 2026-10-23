from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential


def embed_log_message(log_message):
    credential = TextAnalyticsApiKeyCredential('your_text_analytics_api_key')
    client = TextAnalyticsClient(endpoint='https://your-text-analytics-resource.cognitiveservices.azure.com/', credential=credential)
    response = client.extract_key_phrases(documents=[log_message])
    return response[0].key_phrases