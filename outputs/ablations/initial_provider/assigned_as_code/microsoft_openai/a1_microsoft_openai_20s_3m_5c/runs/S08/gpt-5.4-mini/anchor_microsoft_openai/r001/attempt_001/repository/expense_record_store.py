from azure.cosmos import CosmosClient


def expense_record_store(payload, config=None):
    config = config or {}
    client = CosmosClient(config['account_url'], credential=config['account_key'])
    database = client.get_database_client(config['database'])
    container = database.get_container_client(config['container'])
    item = dict(payload.get('record') or {})
    if 'id' not in item:
        item['id'] = payload.get('record_id') or item.get('record_id') or 'expense-record'
    stored = container.upsert_item(item)
    return {'stored': True, 'record': stored}
