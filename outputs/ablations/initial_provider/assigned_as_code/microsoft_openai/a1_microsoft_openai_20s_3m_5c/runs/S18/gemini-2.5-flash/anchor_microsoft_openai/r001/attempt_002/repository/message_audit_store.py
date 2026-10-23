import os
from azure.cosmos import CosmosClient, PartitionKey

def persist_message_record(message_id: str, payload: dict, status: str, processing_details: dict):
    url = os.environ.get("AZURE_COSMOS_DB_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_DB_KEY")
    database_name = os.environ.get("AZURE_COSMOS_DB_DATABASE_NAME", "MessageAuditDB")
    container_name = os.environ.get("AZURE_COSMOS_DB_CONTAINER_NAME", "MessageRecords")

    if not url or not key:
        raise ValueError("AZURE_COSMOS_DB_ENDPOINT or AZURE_COSMOS_DB_KEY environment variables not set.")

    client = CosmosClient(url, credential=key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/message_id"),
        offer_throughput=400
    )

    item = {
        'id': message_id,
        'message_id': message_id,
        'payload': payload,
        'status': status,
        'processing_details': processing_details,
        'timestamp': ""
    }
    
    # Update timestamp before creation/upsert. 
    # This avoids issues with creating the timestamp after the fact. 
    import datetime
    item['timestamp'] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    container.upsert_item(body=item)

    return {"status": "record_persisted", "message_id": message_id}
