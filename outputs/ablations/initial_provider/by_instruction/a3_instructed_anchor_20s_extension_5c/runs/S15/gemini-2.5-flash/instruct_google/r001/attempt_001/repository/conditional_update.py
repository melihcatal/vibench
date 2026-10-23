from database_client import get_datastore_client
from google.cloud import datastore

def conditional_update(document_id: str, field_to_check: str, expected_value: any, updates: dict):
    client = get_datastore_client()
    key = client.key('Document', document_id)

    with client.transaction():
        entity = client.get(key)
        if not entity:
            return {"status": "not_found", "document_id": document_id}

        if entity.get(field_to_check) == expected_value:
            entity.update(updates)
            client.put(entity)
            return {"status": "success", "document_id": document_id}
        else:
            return {"status": "condition_failed", "document_id": document_id}