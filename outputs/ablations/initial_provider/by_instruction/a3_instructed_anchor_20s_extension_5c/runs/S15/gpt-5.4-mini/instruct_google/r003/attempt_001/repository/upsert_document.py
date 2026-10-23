from google.cloud import firestore

from database_client import get_collection
from database_models import UpsertDocumentRequest, normalize_document


def upsert_document(request: UpsertDocumentRequest):
    document = normalize_document(request.document)
    document_id = str(document.get(request.document_id_field))
    if not document_id:
        raise ValueError("document identifier is required")
    collection = get_collection(request.collection)
    collection.document(document_id).set(document, merge=True)
    return {"collection": request.collection, "document_id": document_id, "status": "upserted"}
