from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from security_models import normalize_text


def payload_safety(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['key']))
    text = normalize_text(payload.get('text'))
    result = client.analyze_sentiment([text])[0]
    return {'safe': result.sentiment != 'negative', 'sentiment': result.sentiment, 'provider': 'azure-ai-textanalytics'}
