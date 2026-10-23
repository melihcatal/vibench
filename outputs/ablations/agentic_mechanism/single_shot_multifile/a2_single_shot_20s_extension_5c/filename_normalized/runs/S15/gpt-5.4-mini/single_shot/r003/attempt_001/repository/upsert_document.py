import os
import boto3
from botocore.exceptions import ClientError
from database_client import get_table_name, get_dynamodb_resource, get_document_id_name
from database_models import normalize_document_payload, UpsertDocumentRequest, upsert_result


def handler(event, context=None):
    request = UpsertDocumentRequest.from_event(event)
    table = get_dynamodb_resource().Table(get_table_name())
    document_id_name = get_document_id_name()
    item = normalize_document_payload(request.document, document_id_name=document_id_name)
    item[document_id_name] = request.document_id
    try:
        table.put_item(Item=item)
        return upsert_result(request.document_id, item)
    except ClientError as exc:
        raise RuntimeError(str(exc))
