from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def record_text_safety(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=AzureKeyCredential(config['text_analytics_key']))
    text = payload['text']
    result = client.analyze_sentiment([text])[0]
    return {'unsafe': result.sentiment == 'negative', 'sentiment': result.sentiment}
