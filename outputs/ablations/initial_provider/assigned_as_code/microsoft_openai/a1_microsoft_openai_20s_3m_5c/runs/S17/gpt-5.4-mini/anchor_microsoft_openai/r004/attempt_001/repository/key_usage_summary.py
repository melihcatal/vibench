from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


def key_usage_summary(payload, config=None):
    config = config or {}
    client = SearchClient(endpoint=config['search_endpoint'], index_name=config['search_index'], credential=AzureKeyCredential(config['search_key']))
    query = payload.get('query', '*')
    results = client.search(query, top=payload.get('top', 5))
    summary = []
    for item in results:
        summary.append({'key_id': item.get('key_id'), 'event': item.get('event_type'), 'count': item.get('count', 0)})
    return {'summary': summary, 'source': 'azure-search'}
