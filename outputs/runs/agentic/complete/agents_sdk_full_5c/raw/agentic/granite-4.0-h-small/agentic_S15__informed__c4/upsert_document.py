import os
from database_client import get_dynamodb_client
from database_models import Item, upsert_item_payload

def upsert_document(identifier: str, data: dict) -> None:
    """Upsert a JSON document into DynamoDB by its primary identifier.
    Uses the local helper to normalize the payload.
    """
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    payload = upsert_item_payload(identifier, data)
    response = client.update_item(**payload)
    print('Upsert response:', response)
