from database_client import get_firestore_client, get_collection_name
from database_models import Document


def upsert_document(document: Document) -> dict:
    db = get_firestore_client()
    collection_ref = db.collection(get_collection_name())
    doc_ref = collection_ref.document(document.id)

    data_to_upsert = document.data
    if document.version is not None:
        data_to_upsert["version"] = document.version

    doc_ref.set(data_to_upsert)
    return {"id": document.id, "status": "upserted"}
