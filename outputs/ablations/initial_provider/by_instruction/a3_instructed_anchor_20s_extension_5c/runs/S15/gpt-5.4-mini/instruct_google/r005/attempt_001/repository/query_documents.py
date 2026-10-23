from database_client import get_collection_name, get_firestore_client


def query_documents(field_name, field_value):
    query = get_firestore_client().collection(get_collection_name()).where(field_name, "==", field_value)
    return [{"document_id": doc.id, "data": doc.to_dict() or {}, "provider": "google_firestore"} for doc in query.stream()]
