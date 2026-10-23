from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential


def translate_log_message(log_message, target_language):
    credential = TextAnalyticsApiKeyCredential('your_text_analytics_api_key')
    client = TextAnalyticsClient(endpoint='https://your-text-analytics-resource.cognitiveservices.azure.com/', credential=credential)
    response = client.translate(documents=[log_message], to=target_language)
    return response[0].translations[0].text