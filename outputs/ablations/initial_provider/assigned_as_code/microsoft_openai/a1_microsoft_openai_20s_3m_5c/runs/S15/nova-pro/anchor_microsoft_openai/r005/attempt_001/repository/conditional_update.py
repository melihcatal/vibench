from azure.cosmos import CosmosClient

from database_client import get_client


def conditional_update(document_id, update_payload, config=None):
    client = get_client(config)
    container = client.get_database_client(config['database']).get_container_client(config['container'])
    item = container.read_item(item=document_id, partition_key=document_id)
    item.update(update_payload)
    return container.upsert_item(item)