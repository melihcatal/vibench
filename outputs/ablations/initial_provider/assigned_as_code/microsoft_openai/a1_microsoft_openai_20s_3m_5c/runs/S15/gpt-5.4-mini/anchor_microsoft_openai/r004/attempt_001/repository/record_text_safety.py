from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def record_text_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    text = payload.get('text') or payload.get('content') or ''
    result = client.analyze_text({"text": text})
    return {'categories': getattr(result, 'categories_analysis', None)}
