from database_client import get_datastore_client

def fetch_document(document_id: str):
    client = get_datastore_client()
    key = client.key('Document', document_id)
    entity = client.get(key)
    if entity:
        return {"status": "success", "document_id": document_id, "data": dict(entity)}
    else:
        return {"status": "not_found", "document_id": document_id}