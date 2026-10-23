from database_client import get_container
from database_models import DocumentUpsertRequest, normalize_document


def upsert_document(request: DocumentUpsertRequest) -> dict:
    container = get_container()
    document = normalize_document(request.document)
    if "id" not in document:
        raise ValueError("document id is required")
    return container.upsert_item(document)
