from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    response = client.analyze_text({'text': payload['text']})
    return {'safety': {'categories': getattr(response, 'categories_analysis', []), 'filtered': getattr(response, 'blocklists_match_results', [])}}
