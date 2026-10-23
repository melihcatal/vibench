from azure.ai.content_safety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def visual_safety_text(payload, config=None):
    config = dict(config or {})
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    text = payload.get('text', '')
    result = client.analyze_text({'text': text})
    return {'unsafe': any(getattr(item, 'severity', 0) > int(config.get('threshold', 2)) for item in result.categories_analysis)}
