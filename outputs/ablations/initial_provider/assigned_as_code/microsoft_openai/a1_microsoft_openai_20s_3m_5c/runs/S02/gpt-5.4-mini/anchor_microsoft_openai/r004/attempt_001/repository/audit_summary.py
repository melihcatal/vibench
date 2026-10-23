from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def audit_summary(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(config['endpoint'], AzureKeyCredential(config['key']))
    documents = [payload.get('summary', '')]
    result = client.extract_summary(documents)[0]
    if result.is_error:
        return {'error': result.error.message}
    return {'summary': ' '.join([s.text for s in result.sentences])}
