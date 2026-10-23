from azure.cosmos import CosmosClient


def store_audit_record(record, config=None):
    config = config or {}
    client = CosmosClient(config['cosmos_endpoint'], credential=config['cosmos_key'])
    container = client.get_database_client(config['cosmos_database']).get_container_client(config['cosmos_container'])
    container.upsert_item(record)
    return {'stored': True, 'id': record.get('id')}
