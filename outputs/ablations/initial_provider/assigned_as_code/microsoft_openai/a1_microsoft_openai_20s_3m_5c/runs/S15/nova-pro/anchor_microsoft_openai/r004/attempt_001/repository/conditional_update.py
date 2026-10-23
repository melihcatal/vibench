from azure.cosmos import CosmosClient

from database_client import get_cosmos_client


def conditional_update(document_id, field, value, condition, config=None):
    client = get_cosmos_client(config)
    container = client.get_database_client(config['database']).get_container_client(config['container'])
    document = container.read_item(item=document_id, partition_key=document_id)
    if condition(document):
        document[field] = value
        container.replace_item(item=document['id'], body=document)
        return document
    else:
        return None