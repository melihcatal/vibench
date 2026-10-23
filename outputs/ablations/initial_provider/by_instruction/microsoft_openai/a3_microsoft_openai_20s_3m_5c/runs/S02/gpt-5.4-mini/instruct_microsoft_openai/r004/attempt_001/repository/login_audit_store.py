from azure.cosmos import CosmosClient


def store_audit_record(endpoint, key, database_name, container_name, record):
    client = CosmosClient(endpoint, credential=key)
    container = client.get_database_client(database_name).get_container_client(container_name)
    return container.upsert_item(record)
