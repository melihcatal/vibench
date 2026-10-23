from database_client import FirestoreClient
from database_models import Document, DocumentUpsertRequest


def upsert_document(request: DocumentUpsertRequest):
    db = FirestoreClient.get_client()
    doc_ref = db.collection("documents").document(request.document.id)
    doc_ref.set(request.document.model_dump(by_alias=True))
    return {"status": "success", "document_id": request.document.id}
