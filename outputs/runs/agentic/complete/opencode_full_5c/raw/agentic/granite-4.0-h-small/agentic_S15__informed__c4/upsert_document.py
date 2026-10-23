import json
from database_client import client
from database_models import DocumentRequest, DocumentResponse


def upsert_document(request: DocumentRequest) -> DocumentResponse:
    """
    Upserts a JSON document in the selected NoSQL store.
    Uses the primary identifier `id`. If the document already exists
    the fields are merged/overwritten.
    """
    coll = (
        client.get_collection()
    )  # concrete provider call - see client (e.g., pymongo.Collection)

    result = coll.replace_one({"id": request["id"]}, request["data"], upsert=True)
    # Build a consistent DocumentResponse
    return DocumentResponse(
        id=request["id"],
        data=(request["data"] if request["data"] is not None else {}),
        version=0,  # version not tracked by this generic abstraction
    )


# Helper to expose a JSON‑compatible payload for callers
if __name__ == "__main__":
    sample = DocumentRequest(
        id="example-123", data={"title": "Demo", "tags": ["demo", "upsert"]}
    )
    print(json.dumps(upsert_document(sample), indent=2))
