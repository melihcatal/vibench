from database_client import get_collection
from database_models import DocumentRequest, DocumentResponse, normalize_document


def upsert_document(
    document_id: str, data: dict, partition_key: str = "default"
) -> DocumentResponse:
    collection = get_collection()

    request = DocumentRequest(
        document_id=document_id,
        data=data,
        partition_key=partition_key,
    )

    payload = request.to_dict()

    existing = collection.find_one({"document_id": document_id})
    if existing:
        current_version = existing.get("version", 0)
        payload["version"] = current_version + 1
    else:
        payload["version"] = 1

    result = collection.replace_one({"document_id": document_id}, payload, upsert=True)

    saved_doc = collection.find_one({"document_id": document_id})
    return normalize_document(saved_doc)
