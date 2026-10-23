from database_client import FirestoreClient
from database_models import Document, DocumentFetchRequest


def fetch_document(request: DocumentFetchRequest):
    db = FirestoreClient.get_client()
    doc_ref = db.collection("documents").document(request.document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document": Document(**doc.to_dict())}
    else:
        return {"status": "not_found", "document_id": request.document_id}
