from database_client import get_collection_name, get_firestore_client
from database_models import build_query_result


def query_documents(payload, config=None):
    config = config or {}
    client = get_firestore_client(config)
    collection = client.collection(get_collection_name(config))
    field = payload["field"]
    value = payload["value"]
    records = []
    for doc in collection.where(field, "==", value).stream():
        records.append({"id": doc.id, "document": doc.to_dict()})
    return build_query_result(records)
