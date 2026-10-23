from database_client import get_collection
from database_models import FetchDocumentRequest


def fetch_document(request: FetchDocumentRequest):
    snapshot = get_collection(request.collection).document(request.document_id).get()
    if not snapshot.exists:
        return None
    return snapshot.to_dict()
