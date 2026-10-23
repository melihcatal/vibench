from database_client import get_datastore_client
from google.cloud import datastore

def upsert_document(document_id: str, document_data: dict):
    client = get_datastore_client()
    key = client.key('Document', document_id)
    entity = datastore.Entity(key=key)
    entity.update(document_data)
    client.put(entity)
    return {"status": "success", "document_id": document_id}