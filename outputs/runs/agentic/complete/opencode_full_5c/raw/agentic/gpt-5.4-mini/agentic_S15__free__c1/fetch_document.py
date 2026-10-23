from database_client import database_config, document_table
from database_models import DocumentResponse, FetchDocumentRequest


def fetch_document(document_id, category=None):
    cfg = database_config()
    key = {cfg["document_primary_key"]: document_id}
    if category is not None:
        key[cfg["document_partition_key"]] = category
    item = document_table().get_item(Key=key).get("Item")
    return DocumentResponse(ok=item is not None, data={"document": item}).__dict__


def handler(event, context=None):
    req = FetchDocumentRequest(
        document_id=event.get("document_id"), category=event.get("category")
    )
    return fetch_document(req.document_id, req.category)
