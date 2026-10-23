import os
from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential


def metric_annotation_safety(payload, config=None):
    config = dict(config or {})
    endpoint = config.get('endpoint') or os.environ['AZURE_TEXT_ANALYTICS_ENDPOINT']
    key = config.get('key') or os.environ['AZURE_TEXT_ANALYTICS_KEY']
    text = payload.get('text', '')
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.analyze_sentiment([text])[0]
    return {'text': text, 'unsafe': result.confidence_scores.negative > 0.7}
