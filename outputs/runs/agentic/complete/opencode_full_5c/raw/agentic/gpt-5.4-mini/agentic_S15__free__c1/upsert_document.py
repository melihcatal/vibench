from boto3.dynamodb.conditions import Attr

from database_client import database_config, document_table
from database_models import DocumentResponse, UpsertDocumentRequest, normalize_document


def upsert_document(document):
    cfg = database_config()
    data = normalize_document(document)
    table = document_table()
    table.put_item(Item=data)
    return DocumentResponse(
        ok=True,
        data={
            cfg["document_primary_key"]: data.get(cfg["document_primary_key"]),
            "document": data,
        },
    ).__dict__


def handler(event, context=None):
    return upsert_document(event.get("document", event))
