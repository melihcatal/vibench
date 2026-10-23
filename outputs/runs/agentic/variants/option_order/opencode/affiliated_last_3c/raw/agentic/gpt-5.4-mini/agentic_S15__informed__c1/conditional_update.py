from database_client import get_container
from database_models import DocumentRequest, DocumentResponse, normalize_document


def conditional_update(document_id, updates, partition_key=None, etag=None):
    container = get_container()
    existing = container.read_item(
        item=document_id, partition_key=partition_key or document_id
    )
    if etag and existing.get("_etag") != etag:
        return DocumentResponse(ok=False, error="etag mismatch").to_dict()
    existing.update(updates)
    request = DocumentRequest(
        id=document_id,
        partition_key=partition_key,
        data=normalize_document(existing),
        etag=etag,
    )
    result = container.replace_item(item=request.id, body=request.data)
    return DocumentResponse(ok=True, document=result).to_dict()
