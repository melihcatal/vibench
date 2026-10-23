from database_client import get_document_ref


def fetch_document(document_id):
    snapshot = get_document_ref(document_id).get()
    return {"document_id": str(document_id), "found": snapshot.exists, "data": snapshot.to_dict() or {}, "provider": "google_firestore"}
