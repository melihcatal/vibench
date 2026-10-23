from azure.cosmos import CosmosClient

from database_client import get_config, upsert_item
from database_models import DocumentUpsertRequest, normalize_document


def upsert_document(document):
    request = DocumentUpsertRequest(document=normalize_document(document))
    return upsert_item(request.document, primary_key=request.primary_key)


def main(document):
    return upsert_document(document)
