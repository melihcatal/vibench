from google.cloud import firestore

from document_client import load_config


def expense_record_store(record, collection_name="expense_records"):
    config = load_config()
    client = firestore.Client(project=None)
    document = client.collection(collection_name).document()
    payload = dict(record)
    payload["model"] = config.model
    document.set(payload)
    return {"id": document.id, "collection": collection_name}
