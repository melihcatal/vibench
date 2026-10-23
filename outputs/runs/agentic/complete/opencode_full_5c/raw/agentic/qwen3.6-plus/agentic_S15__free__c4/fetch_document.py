from database_client import get_collection
from database_models import DocumentResponse, normalize_document


def fetch_document(
    document_id: str, partition_key: str = "default"
) -> DocumentResponse:
    collection = get_collection()

    query = {"document_id": document_id}
    if partition_key:
        query["partition_key"] = partition_key

    raw_doc = collection.find_one(query)

    if raw_doc is None:
        return DocumentResponse(
            document_id=document_id,
            data={},
            partition_key=partition_key,
            version=0,
            found=False,
        )

    return normalize_document(raw_doc)
