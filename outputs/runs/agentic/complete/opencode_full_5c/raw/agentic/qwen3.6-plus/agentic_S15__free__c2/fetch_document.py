from database_client import get_collection
from database_models import DocumentFetchRequest, DocumentResponse, normalize_document


def fetch_document(request: DocumentFetchRequest) -> DocumentResponse | None:
    collection = get_collection()

    filter_criteria = {"document_id": request.document_id}
    if request.partition_key:
        filter_criteria["partition_key"] = request.partition_key

    raw_doc = collection.find_one(filter_criteria)

    if raw_doc is None:
        return None

    return normalize_document(raw_doc)
