from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def log_text_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    text = str(payload.get('text', ''))
    result = client.analyze_text(text=text)
    categories = {}
    for item in result.categories_analysis:
        categories[item.category.name] = item.severity
    return {'safe': all(sev == 0 for sev in categories.values()), 'categories': categories}
