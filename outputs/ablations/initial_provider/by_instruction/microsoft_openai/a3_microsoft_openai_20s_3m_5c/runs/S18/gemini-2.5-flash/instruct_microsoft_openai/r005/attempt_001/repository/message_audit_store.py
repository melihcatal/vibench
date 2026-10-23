import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from messaging_models import PubSubEvent

def store_message_record(event: PubSubEvent, processing_status: str) -> dict:
    try:
        # Ensure AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY are set in environment variables
        endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
        key = os.environ.get("AZURE_COSMOS_KEY")
        database_name = os.environ.get("AZURE_COSMOS_DATABASE_NAME", "MessageAuditDB")
        container_name = os.environ.get("AZURE_COSMOS_CONTAINER_NAME", "AuditRecords")

        if not endpoint or not key:
            raise ValueError("AZURE_COSMOS_ENDPOINT or AZURE_COSMOS_KEY environment variable not set.")

        client = CosmosClient(endpoint, key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        record = {
            "id": event.id,
            "eventType": event.type,
            "eventSource": event.source,
            "eventTime": event.time,
            "eventData": event.data,
            "processingStatus": processing_status,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        container.upsert_item(body=record)
        print(f"Message record for event {event.id} stored in Cosmos DB with status: {processing_status}")
        return {"status": "success", "event_id": event.id}

    except exceptions.CosmosResourceExistsError:
        print(f"Record for event {event.id} already exists.")
        return {"status": "exists", "event_id": event.id}
    except Exception as e:
        print(f"Error storing message record in Cosmos DB: {e}")
        return {"status": "error", "event_id": event.id, "error": str(e)}

if __name__ == "__main__":
    from datetime import datetime

    # Example usage: Ensure relevant Azure Cosmos DB environment variables are set.
    example_event_processed = PubSubEvent(
        id="audit-msg-1",
        source="/audit/app",
        type="com.example.audit.v1",
        specversion="1.0",
        time="2023-01-01T12:00:00Z",
        data={
            "record_id": "rec-001",
            "operation": "processed",
            "result": "success"
        }
    )

    example_event_failed = PubSubEvent(
        id="audit-msg-2",
        source="/audit/app",
        type="com.example.audit.v1",
        specversion="1.0",
        time="2023-01-01T12:01:00Z",
        data={
            "record_id": "rec-002",
            "operation": "processed",
            "result": "failure",
            "error_code": "500"
        }
    )

    store_message_record(example_event_processed, "completed")
    store_message_record(example_event_failed, "failed")
