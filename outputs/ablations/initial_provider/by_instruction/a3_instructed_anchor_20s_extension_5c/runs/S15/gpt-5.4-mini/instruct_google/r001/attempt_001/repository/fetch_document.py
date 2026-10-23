import os

from database_client import get_firestore_client
from database_models import FetchRequest


def fetch_document(request: FetchRequest):
    client = get_firestore_client()
    snapshot = client.collection(request.collection).document(request.document_id).get()
    if not snapshot.exists:
        return {"ok": False, "document": None, "error": "not found"}
    data = snapshot.to_dict() or {}
    data[request.document_id_field] = request.document_id
    return {"ok": True, "document": data}


def main():
    request = FetchRequest(collection=os.getenv("FIRESTORE_COLLECTION", "documents"), document_id="sample")
    return fetch_document(request)


if __name__ == "__main__":
    main()
