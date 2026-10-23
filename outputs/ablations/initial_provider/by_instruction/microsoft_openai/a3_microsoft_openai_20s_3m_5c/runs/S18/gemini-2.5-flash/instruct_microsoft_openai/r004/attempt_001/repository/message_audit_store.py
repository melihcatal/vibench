import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from messaging_models import Event

def persist_message_record(event: Event):
    cosmos_endpoint = os.environ.get("AZURE_COSMOSDB_ENDPOINT")
    cosmos_key = os.environ.get("AZURE_COSMOSDB_KEY")
    database_name = os.environ.get("AZURE_COSMOSDB_DATABASE_NAME", "MessageAuditDB")
    container_name = os.environ.get("AZURE_COSMOSDB_CONTAINER_NAME", "ProcessedMessages")

    if not cosmos_endpoint or not cosmos_key:
        print("Azure Cosmos DB credentials not set. Skipping persistence.")
        return

    client = CosmosClient(cosmos_endpoint, credential=cosmos_key)

    try:
        database = client.create_database_if_not_exists(id=database_name)
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/type"),
            offer_throughput=400
        )

        # Prepare item for Cosmos DB. Cosmos DB requires 'id' field for documents.
        # We can use the event.id as the document ID.
        item = event.dict()
        item["id"] = event.id # Ensure the 'id' field exists for Cosmos DB
        
        container.upsert_item(body=item)
        print(f"Persisted event with ID: {event.id} to Cosmos DB.")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error interacting with Cosmos DB: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    example_event = Event(id="audit_123", type="user_login", data={"user_id": "user456", "timestamp": "2026-09-20T10:00:00Z"})
    persist_message_record(example_event)
