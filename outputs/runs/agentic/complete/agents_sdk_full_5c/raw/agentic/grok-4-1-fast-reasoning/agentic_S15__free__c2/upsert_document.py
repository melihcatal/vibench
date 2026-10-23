from database_client import get_dynamodb_table
from database_models import prepare_upsert_item
from typing import Dict, Any

def upsert_document(identifier: str, document: Dict[str, Any]) -> None:
    table = get_dynamodb_table()
    item = prepare_upsert_item(identifier, document)
    table.put_item(Item=item)