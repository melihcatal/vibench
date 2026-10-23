import os

from google.cloud import firestore

from database_client import get_collection_name, get_firestore_client
from database_models import UpsertRequest, normalize_document


def upsert_document(request: UpsertRequest):
    client = get_firestore_client()
    collection = client.collection(request.collection)
    document = normalize_document(request.document)
    document_id = str(document.get(request.document_id_field) or request.document.get(request.document_id_field))
    if not document_id:
        raise ValueError("missing document identifier")
    document[request.document_id_field] = document_id
    collection.document(document_id).set(document, merge=True)
    return {"ok": True, "document": document}


def main():
    collection = os.getenv("FIRESTORE_COLLECTION", get_collection_name())
    request = UpsertRequest(collection=collection, document={"id": "sample", "name": "example"})
    return upsert_document(request)


if __name__ == "__main__":
    main()
