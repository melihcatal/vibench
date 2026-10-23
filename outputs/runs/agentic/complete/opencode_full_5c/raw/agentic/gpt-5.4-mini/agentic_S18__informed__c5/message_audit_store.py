import os
from azure.cosmos import CosmosClient

def store_message_audit(record):
    endpoint = os.environ['AZURE_COSMOS_ENDPOINT']
    key = os.environ['AZURE_COSMOS_KEY']
    database_name = os.environ.get('AZURE_COSMOS_DATABASE', 'messaging')
    container_name = os.environ.get('AZURE_COSMOS_CONTAINER', 'audit')
    client = CosmosClient(endpoint, credential=key)
    db = client.get_database_client(database_name)
    container = db.get_container_client(container_name)
    return container.upsert_item(record)
