import os
import json
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey

from messaging_models import AuditRecord

def persist_audit_record(record: AuditRecord) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_COSMOS_DB_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_DB_KEY")
    database_id = os.environ.get("AZURE_COSMOS_DB_DATABASE_ID")
    container_id = os.environ.get("AZURE_COSMOS_DB_CONTAINER_ID")

    if not all([endpoint, key, database_id, container_id]):
        raise ValueError("AZURE_COSMOS_DB_ENDPOINT, AZURE_COSMOS_DB_KEY, AZURE_COSMOS_DB_DATABASE_ID, and AZURE_COSMOS_DB_CONTAINER_ID environment variables must be set.")

    client = CosmosClient(url=endpoint, credential=key)
    database = client.get_database_client(database_id)
    container = database.get_container_client(container_id)

    # Cosmos DB expects an 'id' field for each item
    item = {
        "id": record.message_id, # Using message_id as item ID for uniqueness
        "event_payload": record.event_payload,
        "processed_at": record.processed_at,
        "status": record.status,
        "processing_summary": record.processing_summary,
        "safety_check_results": record.safety_check_results,
        "translation_results": record.translation_results,
        "_ts": int(datetime.utcnow().timestamp()) # Add a timestamp for consistent updates
    }

    # Upsert the item (insert if not exists, update if exists)
    response = container.upsert_item(body=item)

    return {"status": "persisted", "message_id": response["id"], "cosmos_db_document_id": response["id"]}
