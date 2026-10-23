from database_client import get_firestore_client
from database_models import UpsertDocumentRequest, UpsertDocumentResponse

def upsert_document(request: UpsertDocumentRequest) -> UpsertDocumentResponse:
    """
    Upserts a JSON document into Google Cloud Firestore.
    """
    db = get_firestore_client()
    doc_ref = db.collection(request.collection_name).document(request.document_id)

    try:
        doc_ref.set(request.document_data)
        return UpsertDocumentResponse(
            success=True,
            document_id=request.document_id,
            message="Document upserted successfully."
        )
    except Exception as e:
        return UpsertDocumentResponse(
            success=False,
            document_id=request.document_id,
            message=f"Error upserting document: {e}"
        )

# Provider-identifying signal: google.cloud.firestore
