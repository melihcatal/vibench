from azure.cosmos import exceptions

from database_client import get_container, normalize_document
from database_models import UpsertDocumentRequest


def upsert_document(request: UpsertDocumentRequest):
    container = get_container()
    document = normalize_document(request.document)
    return container.upsert_item(document)
