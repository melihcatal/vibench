import json
from database_client import client
from database_models import DocumentKey, DocumentResponse


def fetch_document(key: DocumentKey) -> DocumentResponse:
    """
    Retrieves a document by its primary identifier `id`.
    Returns a normalized DocumentResponse or raises if not found.
    """
    coll = client.get_collection()  # concrete provider call (e.g., pymongo.Collection)
    doc = coll.find_one({"id": key["id"]})
    if doc is None:
        raise KeyError(f"Document with id {key['id']} not found")
    # Ensure a consistent shape for downstream code
    return DocumentResponse(
        id=doc["id"], data=doc.get("data", {}), version=doc.get("version", 0)
    )


# Demo usage (executed when run as script)
if __name__ == "__main__":
    key = {"id": "example-123"}
    try:
        resp = fetch_document(key)
        print(json.dumps(resp, indent=2))
    except KeyError as e:
        print(e)
