from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def incident_summary(payload, config=None):
    config = config or {}
    items = payload.get('logs', [])
    texts = [str(item.get('message', '')) for item in items if item.get('message')]
    if not texts:
        return {'summary': '', 'error_count': 0, 'severity': payload.get('severity', 'ERROR')}
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    joined = ' '.join(texts[:10])[:5000]
    summary = client.extract_key_phrases(documents=[joined])[0]
    phrases = summary.key_phrases if not summary.is_error else []
    return {'summary': '; '.join(phrases), 'error_count': len(items), 'severity': payload.get('severity', 'ERROR')}
