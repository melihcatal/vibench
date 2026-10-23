from database_client import get_collection
from database_models import DocumentResponse, to_document_response


def fetch_document(document_id: str) -> DocumentResponse:
    collection = get_collection()
    doc = collection.find_one({"_id": document_id})
    if doc is None:
        return DocumentResponse(
            document_id=document_id,
            data={},
            success=False,
            error="Document not found",
        )
    return to_document_response(doc)
