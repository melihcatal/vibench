import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def ocr_safety(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ['AZURE_LANGUAGE_ENDPOINT']
    api_key = config.get('api_key') or os.environ['AZURE_LANGUAGE_API_KEY']
    with TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key)) as client:
        result = client.analyze_sentiment([payload['text']])[0]
    return {'unsafe': result.confidence_scores.negative > 0.7, 'sentiment': result.sentiment}
