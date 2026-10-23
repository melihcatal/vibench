import json
import sys

from google.cloud import firestore

from database_client import document_ref
from database_models import normalize_document_id, normalize_payload, DocumentResult


def upsert_document(document_id, payload):
    document_id = normalize_document_id(document_id)
    payload = normalize_payload(payload)
    ref = document_ref(document_id)
    ref.set(payload, merge=True)
    return DocumentResult(id=document_id, data=payload)


def main():
    if len(sys.argv) < 3:
        raise SystemExit(1)
    document_id = sys.argv[1]
    payload = json.loads(sys.argv[2])
    result = upsert_document(document_id, payload)
    print(json.dumps({"id": result.id, "data": result.data, "exists": result.exists}))


if __name__ == "__main__":
    main()
