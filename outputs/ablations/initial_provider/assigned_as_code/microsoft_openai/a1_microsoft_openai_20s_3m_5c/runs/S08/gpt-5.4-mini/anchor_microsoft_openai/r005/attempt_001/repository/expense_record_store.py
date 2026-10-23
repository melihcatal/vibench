import os
from azure.cosmos import CosmosClient


def expense_record_store(payload, config=None):
    config = config or {}
    client = CosmosClient(config.get('endpoint') or os.environ.get('AZURE_COSMOS_ENDPOINT'), credential=config.get('key') or os.environ.get('AZURE_COSMOS_KEY'))
    database = client.get_database_client(config['database'])
    container = database.get_container_client(config['container'])
    record = payload.get('record') or {}
    result = container.upsert_item(record)
    return {'stored_record': result}
