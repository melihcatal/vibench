import os
import json
from azure.cosmos import CosmosClient, PartitionKey
from messaging_models import EventMessage


def persist_message_record(
    event: EventMessage, database_name: str, container_name: str
):
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables must be set."
        )

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)

    # Create database and container if they don't exist
    try:
        database.create_container(
            id=container_name, partition_key=PartitionKey(path="/message_id")
        )
    except Exception as e:
        # Assume container already exists if creation fails
        if "Conflict" not in str(e):
            raise

    container = database.get_container_client(container_name)

    item = {
        "id": event.message_id,
        "message_id": event.message_id,  # Redundant but good for partition key if it's not 'id'
        "payload": event.payload,
        "attributes": event.attributes,
        "_ts": os.getenv(
            "TEST_COSMOS_TIMESTAMP", ""
        ),  # For testing purposes, can be removed
    }
    container.upsert_item(body=item)
    print(f"Message record {event.message_id} persisted to Cosmos DB.")


if __name__ == "__main__":
    # Example usage
    db_name = os.getenv("AZURE_COSMOS_DB_NAME", "MessageAuditDB")
    container_name = os.getenv("AZURE_COSMOS_CONTAINER_NAME", "AuditRecords")

    event_to_audit = EventMessage(
        message_id="audit-test-1",
        payload={
            "transaction_id": "TXN-001",
            "status": "completed",
            "service": "payment_gateway",
        },
        attributes={"processed_at": "2026-04-20T12:00:00Z"},
    )
    print(f"Persisting event {event_to_audit.message_id} to Cosmos DB...")
    persist_message_record(event_to_audit, db_name, container_name)
    print("Message audit record stored.")
