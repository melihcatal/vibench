from database_client import get_container
from database_models import DocumentRequest, DocumentResponse, normalize_document


def upsert_document(document):
    payload = normalize_document(document)
    request = DocumentRequest(
        id=payload["id"], partition_key=payload.get("partition_key"), data=payload
    )
    container = get_container()
    result = container.upsert_item(request.data)
    return DocumentResponse(ok=True, document=result).to_dict()
