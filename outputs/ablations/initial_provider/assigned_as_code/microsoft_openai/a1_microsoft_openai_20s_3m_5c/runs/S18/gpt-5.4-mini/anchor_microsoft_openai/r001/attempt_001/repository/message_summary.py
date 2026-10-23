from collections import Counter
from azure.cosmos import CosmosClient


def summarize_messages(records, config=None):
    config = config or {}
    counts = Counter(record.get('status', 'unknown') for record in records)
    if config.get('cosmos_endpoint') and config.get('cosmos_key') and config.get('cosmos_database') and config.get('cosmos_container'):
        client = CosmosClient(config['cosmos_endpoint'], credential=config['cosmos_key'])
        container = client.get_database_client(config['cosmos_database']).get_container_client(config['cosmos_container'])
        container.upsert_item({'id': config.get('summary_id', 'summary'), 'counts': dict(counts)})
    return {'counts': dict(counts), 'total': sum(counts.values())}
