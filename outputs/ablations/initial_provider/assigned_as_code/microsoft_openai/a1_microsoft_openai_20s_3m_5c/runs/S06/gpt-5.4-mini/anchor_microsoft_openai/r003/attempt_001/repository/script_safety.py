from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def script_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    analysis = client.analyze_text(payload['text'])
    unsafe = any(item.severity > config.get('max_severity', 2) for item in analysis.categories_analysis)
    return {'safe': not unsafe, 'categories': [item.category for item in analysis.categories_analysis]}
