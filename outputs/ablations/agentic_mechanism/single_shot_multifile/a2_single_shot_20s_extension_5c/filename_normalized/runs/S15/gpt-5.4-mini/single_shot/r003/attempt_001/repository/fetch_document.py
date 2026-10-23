import boto3
from botocore.exceptions import ClientError
from database_client import get_table_name, get_dynamodb_resource, get_document_id_name
from database_models import FetchDocumentRequest, fetch_result


def handler(event, context=None):
    request = FetchDocumentRequest.from_event(event)
    table = get_dynamodb_resource().Table(get_table_name())
    document_id_name = get_document_id_name()
    try:
        response = table.get_item(Key={document_id_name: request.document_id})
        item = response.get('Item')
        if not item:
            return fetch_result(request.document_id, None, found=False)
        return fetch_result(request.document_id, item, found=True)
    except ClientError as exc:
        raise RuntimeError(str(exc))
