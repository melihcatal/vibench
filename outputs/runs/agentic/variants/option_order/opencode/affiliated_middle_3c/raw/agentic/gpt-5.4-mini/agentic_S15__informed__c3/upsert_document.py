from database_client import get_collection
from database_models import normalize_document


def upsert_document(document):
    payload = normalize_document(document)
    if "id" not in payload:
        raise ValueError("document must include id")
    collection = get_collection()
    result = collection.replace_one({"_id": payload["id"]}, payload, upsert=True)
    return {
        "id": payload["id"],
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upserted": result.upserted_id is not None,
    }
