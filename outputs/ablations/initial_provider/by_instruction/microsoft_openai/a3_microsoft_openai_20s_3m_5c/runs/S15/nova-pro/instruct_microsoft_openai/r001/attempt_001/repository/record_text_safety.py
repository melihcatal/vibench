from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def record_text_safety(endpoint, key, text):
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))
    result = text_analytics_client.analyze_sentiment(documents=[text])[0]
    return result.sentiment