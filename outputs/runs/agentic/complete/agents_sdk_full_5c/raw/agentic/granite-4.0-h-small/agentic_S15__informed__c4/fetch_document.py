import os
from database_client import get_dynamodb_client
from database_models import fetch_item_payload

def fetch_document(identifier: str) -> dict:
    """Fetch a JSON document from DynamoDB by its primary identifier.
    Returns the raw item dict or raises if not found.
    """
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    payload = fetch_item_payload(identifier)
    response = client.get_item(**payload)
    if 'Item' in response:
        return response['Item']
    raise KeyError(f'Document with id={identifier} not found')
