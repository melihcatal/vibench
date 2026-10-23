from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def log_text_safety(payload, config=None):
    client = ContentSafetyClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    response = client.analyze_text(payload['text'])
    return {'severity': getattr(response, 'severity', None), 'blocked': getattr(response, 'blocked', False)}
