from database_client import get_collection
from database_models import FetchDocumentRequest, DocumentResponse, Document


def fetch_document(request: FetchDocumentRequest) -> DocumentResponse:
    collection = get_collection()
    document_id = request.document_id
    doc = collection.find_one({"_id": document_id})
    if doc:
        return DocumentResponse(
            document=Document(**doc), message="Document fetched successfully."
        )
    return DocumentResponse(document=None, message="Document not found.")
