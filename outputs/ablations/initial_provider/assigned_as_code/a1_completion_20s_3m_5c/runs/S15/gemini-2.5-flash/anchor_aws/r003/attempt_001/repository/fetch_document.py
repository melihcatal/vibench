import os
from database_client import get_dynamodb_client
from database_models import Document


def fetch_document(document_id: str, table_name: str, key_field: str = "id", region_name: str = None) -> Document | None:
    dynamodb = get_dynamodb_client(region_name)
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={key_field: document_id})
    item = response.get("Item")
    if item:
        return Document(id=item.pop(key_field), content=item)
    return None
