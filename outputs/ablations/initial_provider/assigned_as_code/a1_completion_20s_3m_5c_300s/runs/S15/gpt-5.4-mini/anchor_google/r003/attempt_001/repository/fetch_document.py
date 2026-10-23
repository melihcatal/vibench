from database_client import get_collection_name, get_firestore_client
from database_models import build_record_result


def fetch_document(payload, config=None):
    config = config or {}
    client = get_firestore_client(config)
    doc = client.collection(get_collection_name(config)).document(payload["id"]).get()
    data = doc.to_dict() if doc.exists else None
    return build_record_result(payload["id"], data)
