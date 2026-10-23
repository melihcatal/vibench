from database_client import get_table
from database_models import (
    DocumentUpsertRequest,
    extract_document_id,
    normalize_document,
)


def upsert_document(request: DocumentUpsertRequest):
    table = get_table()
    document = normalize_document(request.document)
    document_id = extract_document_id(document, request.id_field)
    document[request.id_field] = document_id
    table.put_item(Item=document)
    return document
