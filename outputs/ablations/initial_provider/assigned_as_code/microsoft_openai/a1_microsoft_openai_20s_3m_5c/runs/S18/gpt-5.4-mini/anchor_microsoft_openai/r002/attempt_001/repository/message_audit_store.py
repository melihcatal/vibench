from azure.cosmos import CosmosClient


def message_audit_store(record, config=None):
    cfg = config or {}
    client = CosmosClient(cfg['endpoint'], credential=cfg['key'])
    database = client.get_database_client(cfg['database'])
    container = database.get_container_client(cfg['container'])
    container.upsert_item(record)
    return {'stored': True, 'id': record.get('id')}
