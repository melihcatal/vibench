import os
from azure.cosmos import CosmosClient, PartitionKey
from messaging_models import EventMessage

def audit_store_message(message: EventMessage, config=None):
    config = config or {}
    url = config.get('url', os.environ.get("AZURE_COSMOS_DB_URL"))
    key = config.get('key', os.environ.get("AZURE_COSMOS_DB_KEY"))
    database_name = config.get('database_name', os.environ.get("AZURE_COSMOS_DB_DATABASE_NAME"))
    container_name = config.get('container_name', os.environ.get("AZURE_COSMOS_DB_CONTAINER_NAME"))

    if not all([url, key, database_name, container_name]):
        raise ValueError("Azure Cosmos DB URL, key, database name, and container name must be provided.")

    client = CosmosClient(url, credential=key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    item = {
        "id": message.event_id,
        "event_type": message.event_type,
        "data": message.data,
        "attributes": message.attributes,
        "_partitionkey": message.event_id # Using event_id as partition key for simplicity
    }

    container.upsert_item(body=item)

    return {"status": "audited", "message_id": message.event_id}
