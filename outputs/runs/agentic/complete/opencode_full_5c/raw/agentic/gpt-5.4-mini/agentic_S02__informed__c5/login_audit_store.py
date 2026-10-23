from azure.cosmos import CosmosClient
import os


def store_audit_record(record: dict) -> None:
    client = CosmosClient(
        os.environ.get("AZURE_COSMOS_ENDPOINT", ""),
        credential=os.environ.get("AZURE_COSMOS_KEY", ""),
    )
    db = client.get_database_client(os.environ.get("AZURE_COSMOS_DATABASE", "audit"))
    container = db.get_container_client(
        os.environ.get("AZURE_COSMOS_CONTAINER", "login_events")
    )
    container.upsert_item(record)
