from database_client import get_collection


def fetch_document(document_id: str) -> dict:
    snapshot = get_collection().document(document_id).get()
    if not snapshot.exists:
        return {"document_id": document_id, "found": False, "data": {}}
    return {"document_id": document_id, "found": True, "data": snapshot.to_dict() or {}}
