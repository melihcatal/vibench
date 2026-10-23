from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def payload_safety(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=AzureKeyCredential(config['text_analytics_key']))
    documents = [payload.get('text', '')]
    response = client.analyze_sentiment(documents)
    sentiment = response[0].sentiment if response else 'unknown'
    unsafe = sentiment in ('negative', 'mixed') or any(term in payload.get('text', '').lower() for term in ('malware', 'credential', 'exfiltrate'))
    return {'unsafe': unsafe, 'sentiment': sentiment, 'provider': 'azure-ai-textanalytics'}
