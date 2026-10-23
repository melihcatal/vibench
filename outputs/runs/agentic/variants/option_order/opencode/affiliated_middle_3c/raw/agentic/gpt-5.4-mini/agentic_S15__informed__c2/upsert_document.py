from database_client import get_table
from database_models import (
    DocumentRequest,
    DocumentResponse,
    normalize_document,
    normalize_identifier,
)


def upsert_document(payload):
    request = DocumentRequest(document=normalize_document(dict(payload)))
    identifier = normalize_identifier(
        request.document.get("id") or request.document.get("_id")
    )
    request.document["id"] = identifier
    get_table().put_item(Item=request.document)
    return DocumentResponse(ok=True, document=request.document, message="upserted")
