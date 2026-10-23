from azure.cosmos import CosmosClient, PartitionKey
import os
import json
from datetime import datetime

def store_message_audit_record(record: dict):
    """
    Persists a processed message audit record to Azure Cosmos DB.
    The record should include at least 'id' and 'processed_at' fields.
    """
    url = os.environ.get("AZURE_COSMOS_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_KEY")
    database_name = os.environ.get("AZURE_COSMOS_DATABASE_NAME", "MessageAuditDB")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER_NAME", "AuditRecords")

    if not all([url, key]):
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables must be set.")

    client = CosmosClient(url, credential=key)
    database = client.create_database_if_not_exists(id=database_name)

    # We'll use 'message_id' from the record as the partition key for simplicity,
    # or a more generic 'record_type' if messages can have different structures.
    # For this example, let's assume 'id' in the record is unique and can serve as partition key.
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id"), # Assuming 'id' is present in the record for partition
        offer_throughput=400
    )

    # Ensure the record has an 'id' for Cosmos DB item ID and partition key
    if "id" not in record:
        if "message_id" in record:
            record["id"] = record["message_id"]
        else:
            record["id"] = str(uuid.uuid4()) # Generate a unique ID if not provided

    if "processed_at" not in record:
        record["processed_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        container.upsert_item(body=record)
        print(f"Successfully stored audit record for message ID: {record.get('id', 'N/A')}")
    except Exception as e:
        print(f"Error storing audit record in Cosmos DB: {e}")

if __name__ == "__main__":
    import uuid
    # Example usage
    sample_audit_record = {
        "message_id": "order-abc-123",
        "event_type": "OrderProcessed",
        "status": "completed",
        "processor_version": "1.0.0",
        "metadata": {"source": "pubsub", "consumer_group": "web_app"}
    }
    store_message_audit_record(sample_audit_record)

    sample_audit_record_2 = {
        "id": "user-reg-456", # Explicitly providing 'id'
        "event_type": "UserRegistered",
        "status": "failed",
        "error_details": "Invalid email format",
        "processor_version": "1.0.1"
    }
    store_message_audit_record(sample_audit_record_2)
