from azure.cosmos import CosmosClient
import os


def expense_record_store(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ.get('AZURE_COSMOS_ENDPOINT')
    key = config.get('api_key') or os.environ.get('AZURE_COSMOS_KEY')
    database = config.get('database') or 'expenses'
    container = config.get('container') or 'records'
    client = CosmosClient(endpoint, key)
    db = client.get_database_client(database)
    cont = db.get_container_client(container)
    item = payload.get('record', {})
    cont.upsert_item(item)
    return {'stored': True, 'id': item.get('id')}
