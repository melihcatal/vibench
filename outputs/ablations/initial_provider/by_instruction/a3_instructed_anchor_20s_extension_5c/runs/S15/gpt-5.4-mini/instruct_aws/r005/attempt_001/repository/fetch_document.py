from database_client import dynamodb_table
from database_models import document_key, record_response


def fetch_document(document_id):
    response = dynamodb_table().get_item(Key=document_key(document_id))
    return record_response(response.get("Item"))


def handler(event, context=None):
    return fetch_document(event["document_id"])
