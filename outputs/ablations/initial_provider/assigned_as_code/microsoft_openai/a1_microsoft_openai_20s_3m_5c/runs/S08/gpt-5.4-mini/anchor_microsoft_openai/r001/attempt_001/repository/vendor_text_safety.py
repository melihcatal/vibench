from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def vendor_text_safety(payload, config=None):
    config = config or {}
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.analyze_text({'text': payload.get('text', '')})
    return {'safe': all((category.severity or 0) < config.get('max_severity', 2) for category in result.categories), 'categories': [{'category': c.category, 'severity': c.severity} for c in result.categories]}
