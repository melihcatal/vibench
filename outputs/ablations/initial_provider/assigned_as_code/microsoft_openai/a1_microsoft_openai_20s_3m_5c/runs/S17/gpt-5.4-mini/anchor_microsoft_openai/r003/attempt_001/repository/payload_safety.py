from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def payload_safety(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    response = client.analyze_sentiment([payload['text']])[0]
    return {'unsafe': response.confidence_scores.negative > 0.7, 'sentiment': response.sentiment}
