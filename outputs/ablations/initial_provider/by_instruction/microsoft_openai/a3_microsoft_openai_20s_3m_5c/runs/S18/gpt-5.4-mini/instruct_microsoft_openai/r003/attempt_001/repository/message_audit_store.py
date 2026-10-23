from azure.cosmos import CosmosClient


def store_message_record(endpoint, key, database_name, container_name, record):
    client = CosmosClient(endpoint, credential=key)
    container = client.get_database_client(database_name).get_container_client(container_name)
    container.upsert_item(record)
    return {"stored": True, "id": record.get("id")}
