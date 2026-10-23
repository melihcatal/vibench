import os
from typing import Any, Dict, Optional

from google.cloud import firestore


def fetch_document(document_id: str, collection_name: Optional[str] = None) -> Dict[str, Any]:
    collection = collection_name or os.environ.get("FIRESTORE_COLLECTION", "documents")
    client = firestore.Client()
    doc = client.collection(collection).document(document_id).get()
    if not doc.exists:
        raise KeyError(document_id)
    data = doc.to_dict() or {}
    data["id"] = doc.id
    return data


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: fetch_document.py DOCUMENT_ID [COLLECTION_NAME]")
    document_id = sys.argv[1]
    collection_name = sys.argv[2] if len(sys.argv) > 2 else None
    print(json.dumps(fetch_document(document_id, collection_name), sort_keys=True))
