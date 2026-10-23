from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    text = payload.get('text', '')
    result = client.analyze_text({'text': text})
    return {'label': getattr(result, 'category', None), 'severity': getattr(result, 'severity', None), 'text': text}
