from database_client import get_collection
from database_models import DocumentFetchResponse


def fetch_document(document_id: str) -> DocumentFetchResponse:
    collection = get_collection()
    raw = collection.find_one({"_id": document_id})
    if raw is None:
        return DocumentFetchResponse.not_found(document_id)
    return DocumentFetchResponse.from_mongo_document(raw)


def fetch_document_raw(document_id: str) -> dict:
    response = fetch_document(document_id)
    return response.to_dict()


if __name__ == "__main__":
    result = fetch_document_raw("doc-001")
    print(result)
