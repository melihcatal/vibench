import sys

from google.cloud import firestore

from database_client import get_collection
from database_models import DocumentRequest, normalize_document


def upsert_document(request: DocumentRequest) -> dict:
    collection = get_collection()
    payload = normalize_document(request.data)
    collection.document(request.document_id).set(payload, merge=True)
    return {"document_id": request.document_id, "upserted": True, "data": payload}


if __name__ == "__main__":
    raise SystemExit(0)
