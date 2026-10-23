from database_client import get_collection_ref
from database_models import normalize_document


def query_documents(payload, config=None):
    config = config or {}
    payload = normalize_document(payload)
    field = payload["field"]
    value = payload["value"]
    results = []
    for snapshot in get_collection_ref(config).where(field, "==", value).stream():
        results.append({"id": snapshot.id, "document": snapshot.to_dict()})
    return {"documents": results}
