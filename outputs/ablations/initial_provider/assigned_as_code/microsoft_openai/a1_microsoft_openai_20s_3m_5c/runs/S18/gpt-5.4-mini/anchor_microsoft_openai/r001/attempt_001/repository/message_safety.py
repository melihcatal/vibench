from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def check_message_safety(text, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=AzureKeyCredential(config['text_analytics_key']))
    response = client.analyze_sentiment([text])[0]
    return {'unsafe': response.sentiment == 'negative', 'sentiment': response.sentiment}
