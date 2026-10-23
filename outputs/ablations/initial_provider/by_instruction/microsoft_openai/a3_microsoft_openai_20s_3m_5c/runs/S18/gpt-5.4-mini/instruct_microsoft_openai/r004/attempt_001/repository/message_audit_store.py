import os

from azure.cosmos import CosmosClient


def message_audit_store(record):
    client = CosmosClient(os.environ["AZURE_COSMOS_ENDPOINT"], credential=os.environ["AZURE_COSMOS_KEY"])
    database = client.get_database_client(os.environ.get("AZURE_COSMOS_DATABASE", "messaging"))
    container = database.get_container_client(os.environ.get("AZURE_COSMOS_CONTAINER", "audit"))
    container.upsert_item(record)
    return {"stored": True}
