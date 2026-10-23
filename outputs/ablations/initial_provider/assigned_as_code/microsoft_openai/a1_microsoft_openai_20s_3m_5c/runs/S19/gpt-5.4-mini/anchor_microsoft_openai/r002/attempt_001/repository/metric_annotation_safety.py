import re
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def metric_annotation_safety(payload, config=None):
    endpoint = (config or {}).get('endpoint') or payload.get('endpoint')
    key = (config or {}).get('api_key') or payload.get('api_key')
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    text = payload['text']
    categories = []
    if re.search(r'\b(password|secret|token|apikey)\b', text, re.I):
        categories.append('credential')
    if re.search(r'http[s]?://', text, re.I):
        categories.append('url')
    if len(client.analyze_sentiment([text])[0].warnings) if hasattr(client.analyze_sentiment([text])[0], 'warnings') else False:
        categories.append('warning')
    return {'safe': not categories, 'categories': categories}
