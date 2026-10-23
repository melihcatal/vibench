from azure.cosmos import CosmosClient
from database_models import normalize_document


def record_summary(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    doc = normalize_document(document)
    return {'summary': {'id': doc.get('id'), 'title': doc.get('title'), 'status': doc.get('status')}}
