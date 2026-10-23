from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def metric_annotation_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    response = client.analyze_text(payload['text'])
    return {'flagged': any(item.severity >= config.get('threshold', 2) for item in response.categories_analysis)}
