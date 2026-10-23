import json
import os
from typing import Any, Dict, List, Optional

from google.cloud import firestore


FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "documents")


def query_documents(field_name: str, field_value: Any, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
    collection = collection_name or FIRESTORE_COLLECTION
    client = firestore.Client()
    query = client.collection(collection).where(field_name, "==", field_value)
    results: List[Dict[str, Any]] = []
    for snapshot in query.stream():
        data = snapshot.to_dict() or {}
        data["id"] = snapshot.id
        results.append(data)
    return results


def main() -> None:
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: query_documents.py FIELD_NAME FIELD_VALUE [COLLECTION_NAME]")
    field_name = sys.argv[1]
    field_value = sys.argv[2]
    collection_name = sys.argv[3] if len(sys.argv) > 3 else None
    print(json.dumps(query_documents(field_name, field_value, collection_name), sort_keys=True))


if __name__ == "__main__":
    main()
