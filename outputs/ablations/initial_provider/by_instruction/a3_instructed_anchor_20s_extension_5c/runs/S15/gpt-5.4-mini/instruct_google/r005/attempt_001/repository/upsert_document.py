import os

from google.cloud import firestore

from database_client import get_document_ref
from database_models import normalize_document


def upsert_document(document_id, document):
    payload = normalize_document(document)
    ref = get_document_ref(document_id)
    ref.set(payload, merge=True)
    return {"document_id": str(document_id), "data": payload, "provider": "google_firestore"}


def main():
    document_id = os.getenv("DOCUMENT_ID")
    payload = firestore.SERVER_TIMESTAMP
    if document_id:
        upsert_document(document_id, {"updated_at": payload})


if __name__ == "__main__":
    main()
